from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

@tool
def web_search_agent(query: str) -> dict:
    """Searches the web using SerpAPI and summarizes the result with Gemini."""
    
    # Step 1: Perform search using SerpAPI
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 5,
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    # Step 2: Extract relevant snippets
    snippets = []
    for result in data.get("organic_results", []):
        if "snippet" in result:
            snippets.append(result["snippet"])
    snippet_text = "\n".join(snippets[:5]) or "No relevant search results found."

    # Step 3: Summarize with Gemini
    prompt = f"Based on the following web search results, provide a concise summary for the query: {query}\n\n{snippet_text}"
    summary = llm.invoke(prompt).content

    return {"intermediate_result": summary}
