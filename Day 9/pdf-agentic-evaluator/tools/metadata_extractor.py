from langchain.tools import tool
from utils.pdf_utils import extract_pdf_metadata

@tool
def metadata_tool(file_path: str = "paper.pdf") -> str:
    """Extract metadata from a research paper PDF (title, authors, abstract, keywords)"""
    return extract_pdf_metadata(file_path)
