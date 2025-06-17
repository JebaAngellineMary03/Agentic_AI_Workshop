from llm_config import llm

def estimate_impact(text: str) -> str:
    prompt = f"""
Based on the abstract and content, briefly assess the following aspects of the research paper:

Return the output in this markdown table format with short one-line summaries:

| Aspect | Assessment |
|--------|------------|
| 🆕 Novelty | ... |
| 🧠 Technical Depth | ... |
| 📚 Scholarly Impact | ... |
| 📊 Experiments/Data | ... |

Use concise bullet-style phrasing. Avoid overly detailed analysis.

{text[:3000]}
"""
    return llm.invoke(prompt).content
