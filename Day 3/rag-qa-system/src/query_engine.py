# src/query_engine.py

from src.retriever import load_faiss_index, retrieve_relevant_chunks
from answer_generator import generate_answer

def query_rag(query):
    index, chunks = load_faiss_index()
    top_chunks = retrieve_relevant_chunks(query, index, chunks, top_k=5)
    answer = generate_answer(query, top_chunks)

    return {
        "answer": answer,
        "sources": top_chunks
    }
