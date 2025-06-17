import os
import re
from tavily import TavilyClient
from llm_config import llm
from dotenv import load_dotenv

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def extract_abstract(text):
    match = re.search(r'(?i)abstract\s*[:\-]?\s*(.*?)(\n[A-Z][^\n]{5,30}\n|\Z)', text, re.DOTALL)
    return match.group(1).strip() if match else text[:500]

# If abstract is too long, take only the first few sentences (approx. 400 chars)
import re

def truncate_to_sentences(text, limit=400):
    sentences = re.split(r'(?<=[.!?]) +', text)
    result = ''
    for sentence in sentences:
        if len(result) + len(sentence) <= limit:
            result += sentence + ' '
        else:
            break
    return result.strip()

def retrieve_similar_papers(query: str) -> str:
    query = truncate_to_sentences(query, limit=400)

    results = tavily.search(query=query, search_depth="advanced", max_results=3)
    summary = ""
    for idx, r in enumerate(results["results"], 1):
        summary += f"### Paper {idx}: {r['title']}\n"
        summary += f"- 🔗 URL: {r['url']}\n"
        summary += f"- 📄 Snippet: {r['content'][:300]}...\n\n"
    return summary

def benchmark_paper(text: str) -> str:
    abstract = extract_abstract(text)
    retrieved = retrieve_similar_papers(abstract)

    prompt = f"""
You are a Research Benchmarking Agent.

Given the following abstract and retrieved similar papers, briefly compare in 2–3 lines:
1. How relevant are the retrieved papers?
2. How original or high-quality is this work compared to them?
You may include an example paper and a rough % similarity estimate.

### Abstract to Benchmark:
{abstract}

### Retrieved Related Papers:
{retrieved}

Respond only with 2–3 sentences. No tables.
"""

    return llm.invoke(prompt).content
