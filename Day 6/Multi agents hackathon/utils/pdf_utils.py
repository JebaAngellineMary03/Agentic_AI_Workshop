import fitz  # PyMuPDF

def extract_pdf_text(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text
