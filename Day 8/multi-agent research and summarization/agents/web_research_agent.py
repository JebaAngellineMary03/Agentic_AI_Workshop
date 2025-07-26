from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

@tool
def web_search_agent(query: str) -> dict:
    """Searches the web for the given query and summarizes the result."""
    prompt = f"Search the web and summarize this topic: {query}"
    return {"intermediate_result": llm.invoke(prompt).content}