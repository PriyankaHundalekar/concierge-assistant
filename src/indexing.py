import os
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100):
    """Simple sliding window chunker preserving local context."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def build_vector_store(raw_docs_dir: str = "data/raw_docs", db_path: str = "data/chroma_db"):
    """Indexes all raw documents into ChromaDB with rich metadata."""
    path = Path(raw_docs_dir)
    if not path.exists():
        raise FileNotFoundError(f"Raw documents directory {raw_docs_dir} does not exist.")

    # Initialize Chroma client and embedding model
    client = chromadb.PersistentClient(path=db_path)
    collection_name = "concierge_docs"
    
    # Reset collection if it exists for clean rebuilds
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
        
    collection = client.create_collection(name=collection_name)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    documents = []
    metadatas = []
    ids = []
    
    doc_id_counter = 0
    for file_path in path.glob("*.*"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        file_name = file_path.name
        chunks = chunk_text(content)
        
        for idx, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "source": file_name,
                "chunk_index": idx,
                "category": "policy" if "policy" in file_name.lower() else "general"
            })
            ids.append(f"doc_{doc_id_counter}_chunk_{idx}")
            doc_id_counter += 1

    if documents:
        print(f"Embedding {len(documents)} chunks across documents...")
        embeddings = embedder.encode(documents, show_progress_bar=True).tolist()
        
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully indexed {len(documents)} chunks into ChromaDB at '{db_path}'.")
    else:
        print("No documents found to index.")

if __name__ == "__main__":
    build_vector_store()