import asyncio
import os
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# 👇 Ensure there's an event loop for the current thread (fix for gRPC async)
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

def rag_search_agent(query: str) -> dict:
    try:
        # Re-ensure event loop for inner gRPC client too
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        # Load vector store
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = db.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        if not context.strip():
            return {"intermediate_result": "No relevant data found in the dataset."}

        prompt = f"""You are a helpful assistant. Use the context below to answer the query:

Context:
{context}

Query: {query}
"""

        response = llm.invoke(prompt)
        summary = getattr(response, "content", str(response)).strip()

        return {"intermediate_result": summary or "No summary generated from RAG."}

    except Exception as e:
        print("❌ Error in rag_search_agent:", e)
        return {"intermediate_result": f"Error during RAG: {str(e)}"}
