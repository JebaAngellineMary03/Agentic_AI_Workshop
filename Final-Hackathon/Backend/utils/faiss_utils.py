from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import json
import os

def create_faiss_index_from_json(json_path: str, api_key: str):
    with open(json_path) as f:
        data = json.load(f)
        
    docs = [Document(page_content=item['content'], metadata={"title": item['title']}) for item in data]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    return FAISS.from_documents(docs, embeddings)

def get_faiss_retriever():
    return FAISS.load_local(
        "faiss_index",
        GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")),
        allow_dangerous_deserialization=True
    ).as_retriever()