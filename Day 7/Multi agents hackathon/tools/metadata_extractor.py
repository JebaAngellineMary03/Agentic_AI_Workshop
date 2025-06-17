from llm_config import llm

def extract_metadata(text: str) -> str:
    prompt = f"""
You are a research metadata extractor. Given this paper text, extract:

- Title
- Abstract
- Authors
- Authorship positions
- Conference/Journal
- Keywords
- Year
- DOI (if any)

Only return results in neat bullet format.

{text[:3000]}
"""
    return llm.invoke(prompt).content
