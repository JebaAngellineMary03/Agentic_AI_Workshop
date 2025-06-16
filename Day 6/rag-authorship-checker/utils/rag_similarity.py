import requests
import re
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read API keys from environment
GEMINI_API_KEY2 = os.getenv("GEMINI_API_KEY2")

def fetch_similar_papers(query, num_results=5):
    url = "https://api.openalex.org/works"
    params = {
        "filter": f"title.search:{query}",
        "per-page": num_results
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def reconstruct_openalex_abstract(abstract_dict):
    if not abstract_dict:
        return ""
    words = sorted([(index, word) for word, indices in abstract_dict.items() for index in indices])
    sorted_words = [word for index, word in sorted(words)]
    return " ".join(sorted_words)

def generate_comparison(prompt_text, context_abstracts):
    genai.configure(api_key=GEMINI_API_KEY2)
    model = genai.GenerativeModel("gemini-2.0-flash")
    full_prompt = f"""
You are a research originality evaluator.

Given a research abstract and a group of similar research abstracts, estimate the similarity of the query abstract to the others.

Only respond with a single number from 0 to 100 indicating the **percentage similarity**, where:
- 0 means completely original
- 100 means completely overlapping

Respond with only the number. No extra explanation.

Query Abstract:
{prompt_text}

Similar Research Abstracts:
{context_abstracts}
"""
    response = model.generate_content(full_prompt)
    match = re.search(r"\d{1,3}", response.text)
    return int(match.group()) if match else "Similarity not determined"
