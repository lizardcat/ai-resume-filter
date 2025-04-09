import os
import docx
import fitz  # PyMuPDF

def parse_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"[❌ DOCX error] {path}: {e}")
        return ""

def parse_pdf(path):
    try:
        text = ""
        with fitz.open(path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"[❌ PDF error] {path}: {e}")
        return ""

def extract_resume_text(path):
    filename = os.path.basename(path).lower()
    print(f"[DEBUG] Extracting from: {filename}")

    if filename.endswith('.pdf'):
        return parse_pdf(path)
    elif filename.endswith('.docx'):
        return parse_docx(path)
    else:
        print(f"[❌ Unsupported format] {filename}")
        return ""
