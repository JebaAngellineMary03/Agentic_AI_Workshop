from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from utils.pdf_utils import extract_pdf_text

def benchmark_against_rag(pdf_path):
    text = extract_pdf_text(pdf_path)
    chunks = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(docs, embeddings)

    similar = db.similarity_search(text[:500], k=2)
    return "[RAG Benchmark]\n" + "\n---\n".join([doc.page_content[:300] for doc in similar])
