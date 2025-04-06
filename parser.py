
import docx
import fitz  # PyMuPDF

def parse_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def parse_pdf(file):
    file.seek(0)  
    with fitz.open(stream=file.read(), filetype='pdf') as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
        return text


def extract_resume_text(file):
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        return parse_pdf(file)
    elif filename.endswith('.docx'):
        return parse_docx(file)
    return None
