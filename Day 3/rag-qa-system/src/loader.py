import os
import fitz  

def load_pdfs_from_directory(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            documents.append({"filename": filename, "text": text})
    return documents
