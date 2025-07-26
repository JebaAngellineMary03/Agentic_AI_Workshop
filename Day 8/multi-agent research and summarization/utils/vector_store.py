from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

# ✅ Load .env file
load_dotenv()

# ✅ Read text file
with open("data/dataset.txt", "r", encoding="utf-8") as file:
    texts = file.read()

# ✅ Split into chunks
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = [Document(page_content=chunk) for chunk in splitter.split_text(texts)]

# ✅ Load Gemini API key from .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in environment. Please set it in .env.")

# ✅ Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)

# ✅ Build and save FAISS index
db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index")

print("✅ FAISS index created and saved successfully.")
