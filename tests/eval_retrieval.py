import json
from pathlib import Path
from src.retriever import ConciergeRetriever

def evaluate_retrieval(eval_path: str = "data/eval_set.json", top_k: int = 3):
    if not Path(eval_path).exists():
        print(f"Eval dataset not found at {eval_path}.")
        return

    with open(eval_path, "r", encoding="utf-8") as f:
        eval_cases = json.load(f)

    retriever = ConciergeRetriever()
    
    hits = 0
    reciprocal_ranks = []
    total_evals = len(eval_cases)

    if total_evals == 0:
        print("Evaluation set is empty.")
        return

    for case in eval_cases:
        query = case["question"]
        expected_sources = case["expected_doc_ids"]
        
        # Out-of-bounds questions expect no relevant docs retrieved
        if not expected_sources:
            # If expected sources is empty, we test if retriever pulls nothing or irrelevant info
            continue

        results = retriever.retrieve(query, top_k=top_k)
        retrieved_sources = [r["source"] for r in results]

        # Check Hit Rate (Any expected source in retrieved sources)
        hit_found = False
        first_rank = None
        
        for rank, source in enumerate(retrieved_sources, start=1):
            if source in expected_sources:
                hit_found = True
                if first_rank is None:
                    first_rank = rank

        if hit_found:
            hits += 1
            reciprocal_ranks.append(1.0 / first_rank)
        else:
            reciprocal_ranks.append(0.0)

    # Exclude out of bounds from standard hit rate calculation
    valid_evals = sum(1 for c in eval_cases if c["expected_doc_ids"])
    hit_rate = (hits / valid_evals) * 100 if valid_evals > 0 else 0.0
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0

    print("==============================")
    print(f"RETRIEVAL EVALUATION RESULTS (Top-{top_k})")
    print("==============================")
    print(f"Total Evaluated: {valid_evals}")
    print(f"Hit Rate @ {top_k}: {hit_rate:.2f}%")
    print(f"Mean Reciprocal Rank (MRR): {mrr:.4f}")
    print("==============================")

if __name__ == "__main__":
    evaluate_retrieval()