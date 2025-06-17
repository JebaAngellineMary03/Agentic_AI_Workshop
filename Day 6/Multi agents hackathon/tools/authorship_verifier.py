from llm_config import llm

def verify_authorship(text: str) -> str:
    prompt = f"""
Based on this text, assess whether it is:

- Human-authored
- AI-generated
- Mixed

Give reasoning based on structure, vocabulary, tone, and consistency.

{text[:2500]}
"""
    return llm.invoke(prompt).content
