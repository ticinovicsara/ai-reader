import PyPDF2
from docx import Document

def read_pdf(path):
    reader = PyPDF2.PdfReader(path)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            texts.append(text)
    return "\n".join(texts)

def read_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_file(path):
    if path.endswith(".pdf"):
        return read_pdf(path)
    elif path.endswith(".docx"):
        return read_docx(path)
    elif path.endswith(".txt"):
        return read_txt(path)
    else:
        raise ValueError("File format not supported")
