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
    filename = file.name.lower()  # Use file.name instead of file.filename
    print(f"Processing file: {filename}")  # Debugging: Print the filename
    if filename.endswith('.pdf'):
        try:
            return parse_pdf(file)
        except Exception as e:
            print(f"Error parsing PDF: {e}")  # Debugging: Print error
            return None
    elif filename.endswith('.docx'):
        try:
            return parse_docx(file)
        except Exception as e:
            print(f"Error parsing DOCX: {e}")  # Debugging: Print error
            return None
    else:
        print("Unsupported file type")  # Debugging: Print unsupported file type
        return None
