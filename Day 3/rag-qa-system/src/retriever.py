import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_faiss_index(path="vector_store/index.pkl"):
    with open(path, "rb") as f:
        index, chunks = pickle.load(f)
    return index, chunks

def retrieve_relevant_chunks(query, index, chunks, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for i in indices[0]:
        results.append(chunks[i])
    return results

