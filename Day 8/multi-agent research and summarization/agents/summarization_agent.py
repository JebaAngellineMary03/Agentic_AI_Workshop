from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

def summarize_response(state):
    content = state["intermediate_result"]
    prompt = f"Summarize this response concisely:\n{content}"
    summary = llm.invoke(prompt).content
    return {"summary": summary}  # ✅ Return as a dict