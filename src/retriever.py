# src/retriever.py
import chromadb
from sentence_transformers import SentenceTransformer

class ConciergeRetriever:
    def __init__(self, db_dir: str = "data/chroma_db", collection_name: str = "concierge_docs"):
        self.client = chromadb.PersistentClient(path=db_dir)
        self.collection = self.client.get_collection(name=collection_name)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
    def search(self, query: str, top_k: int = 3):
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        retrieved = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            for doc, meta in zip(docs, metas):
                retrieved.append({
                    "content": doc,
                    "source": meta.get("source")
                })
        return retrieved