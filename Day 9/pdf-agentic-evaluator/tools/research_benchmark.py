from langchain.tools import tool
from utils.rag_utils import benchmark_against_rag

@tool
def benchmarking_tool(file_path: str = "paper.pdf") -> str:
    """Benchmark the paper content against similar papers using RAG."""
    return benchmark_against_rag(file_path)
