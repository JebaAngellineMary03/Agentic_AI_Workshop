import fitz  # PyMuPDF

def extract_pdf_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    return f"[PDF Metadata Extractor]\nTitle: Auto-extracted Title\nAuthors: Author A, Author B\nAbstract: {text[:500]}..."

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)
