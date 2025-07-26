from langchain.tools import tool
import requests
import os

@tool
def search_competitors(location: str) -> str:
    """
    Searches for top clothing store competitors and their footfall info in the given location.
    """
    query = f"top clothing stores and peak hours in {location}"
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "location": location
    }

    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        formatted = [f"{i+1}. {r['title']}: {r.get('snippet','No info')}" for i, r in enumerate(results[:5])]
        return "\n".join(formatted)
    else:
        return "Failed to fetch data from SerpAPI."
