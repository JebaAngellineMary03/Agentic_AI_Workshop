from langchain.tools import tool
from utils.pdf_utils import extract_pdf_text
from utils.nlp_utils import detect_ai_written

@tool
def authorship_tool(file_path: str = "paper.pdf") -> str:
    """Verify if content is AI-generated or self-authored."""
    text = extract_pdf_text(file_path)
    return detect_ai_written(text)
