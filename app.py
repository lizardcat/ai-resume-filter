import os
import re
import datetime
import PyPDF2
import docx
import spacy
import pickle
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from fuzzywuzzy import fuzz
from models import db, JobRole

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///roles.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from resumes
def extract_text_from_resume(filepath):
    file_ext = filepath.rsplit(".", 1)[1].lower()
    text = ""

    if file_ext == "pdf":
        with open(filepath, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"

    elif file_ext == "docx":
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif file_ext == "txt":
        with open(filepath, "r", encoding="utf-8") as txt_file:
            text = txt_file.read()

    return text.strip()

# Function to extract details from resumes

nlp = spacy.load("en_core_web_sm")  # Load spaCy NLP model

def extract_resume_details(text):
    gpa_match = re.search(r"GPA[: ]?(\d\.\d)", text, re.IGNORECASE)
    experience_match = re.search(r"(\d+)\s*years? of experience", text, re.IGNORECASE)
    date_match = re.findall(r"(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b \d{4})", text)

    # Extract GPA
    gpa = float(gpa_match.group(1)) if gpa_match else 0.0

    # Extract Experience (if it's explicitly mentioned)
    if experience_match:
        experience = int(experience_match.group(1))
    elif len(date_match) >= 2:  # Check if two dates are found (start & end dates)
        start_year = int(date_match[0].split()[1])  # Extract year from "Month Year"
        end_year = datetime.datetime.now().year if "Present" in text else int(date_match[1].split()[1])
        experience = max(0, end_year - start_year)  # Calculate experience in years
    else:
        experience = 0  # Default if no valid experience is found

    # Extract skills (Simple tokenization)
    skills_match = re.findall(r"\b[A-Za-z+#]+\b", text)
    skills = [skill.lower() for skill in skills_match]

    return {"gpa": gpa, "experience": experience, "skills": skills}

@app.route("/")
def index():
    job_roles = JobRole.query.all()
    roles_dict = {role.title: role.to_dict() for role in job_roles}
    return render_template("filters.html", roles=roles_dict)

@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_files = request.files.getlist("resumes")
    upload_results = []

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            upload_results.append({"filename": filename, "status": "Uploaded successfully!"})
        else:
            upload_results.append({"filename": "Unknown", "status": "Failed to upload"})

    return jsonify({"uploads": upload_results})

# Load trained ML model and vectorizer
with open("resume_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

@app.route("/filter", methods=["POST"])
def filter_resumes():
    gpa_cutoff = float(request.form.get("gpa_cutoff", 0) or 0)
    experience_cutoff = int(request.form.get("experience", 0) or 0)
    must_have = [skill.lower() for skill in request.form.getlist("must_have") if skill]

    matching_resumes = []
    resume_scores = {}

    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        resume_text = extract_text_from_resume(filepath)
        resume_details = extract_resume_details(resume_text)

        extracted_skills = [skill.lower() for skill in resume_details["skills"]]
        extracted_gpa = resume_details["gpa"]
        extracted_experience = resume_details["experience"]

        meets_gpa = extracted_gpa >= gpa_cutoff
        meets_experience = extracted_experience >= experience_cutoff

        has_must_have_skills = True if not must_have else all(
            any(skill in extracted_skills for skill in must_have) for _ in must_have
        )

        if meets_gpa and meets_experience and has_must_have_skills:
            # 🔹 AI Resume Scoring
            resume_vector = vectorizer.transform([resume_text])
            score = model.predict_proba(resume_vector)[0][1]  # Probability of being hired

            matching_resumes.append(filename)
            resume_scores[filename] = round(score * 100, 2)  # Convert to %

    # Sort resumes by AI Score (higher is better)
    sorted_resumes = sorted(resume_scores.items(), key=lambda x: x[1], reverse=True)

    return jsonify({"matching_resumes": sorted_resumes})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/api/job_roles")
def get_job_roles():
    job_roles = JobRole.query.all()
    return jsonify([role.to_dict() for role in job_roles])

if __name__ == "__main__":
    app.run(debug=True)
