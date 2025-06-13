# src/chunker.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = []
    for doc in documents:
        for i, chunk in enumerate(splitter.split_text(doc["text"])):
            chunks.append({
                "text": chunk,
                "filename": doc["filename"],
                "chunk_id": i
            })
    return chunks
