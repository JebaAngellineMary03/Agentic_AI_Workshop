from src.loader import load_pdfs_from_directory
from src.chunker import chunk_documents
from src.vectorizer import embed_chunks
from src.retriever import build_faiss_index
import os

if __name__ == "__main__":
    docs = load_pdfs_from_directory("data/papers")
    print(f"Loaded {len(docs)} documents.")

    chunks = chunk_documents(docs)
    print(f"Chunked into {len(chunks)} segments.")

    embedded_chunks = embed_chunks(chunks)
    print("Embeddings generated.")

    os.makedirs("vector_store", exist_ok=True)
    build_faiss_index(embedded_chunks)
    print("FAISS index created and stored.")
