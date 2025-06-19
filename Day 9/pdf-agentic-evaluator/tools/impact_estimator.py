from langchain.tools import tool

@tool
def impact_tool(text: str = "Simulated Text") -> str:
    """Estimate potential impact of the paper based on basic content heuristics."""
    return "[Impact Estimator] Novelty: High | Collaboration Score: Good | Impact Level: Medium-High"
