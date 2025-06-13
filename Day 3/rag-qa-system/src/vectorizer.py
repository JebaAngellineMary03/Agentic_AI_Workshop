# src/vectorizer.py
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i]
    return chunks
