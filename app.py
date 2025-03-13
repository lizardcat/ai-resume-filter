import os
import re
import PyPDF2
import docx
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from fuzzywuzzy import fuzz
import spacy
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file types

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

filtering_rules = {
    "Software Engineer": {
        "must_have": ["Java", "Spring Boot", "Git", "REST APIs", "Agile", "Unit Testing"],
        "nice_to_have": ["Docker", "Kubernetes", "Microservices", "CI/CD", "GraphQL", "React"],
        "gpa_cutoff": 3.2,
        "min_experience": 2
    },
    "Frontend Developer": {
        "must_have": ["HTML", "CSS", "JavaScript", "React"],
        "nice_to_have": ["Vue.js", "Angular", "Figma"],
        "gpa_cutoff": 3.0,
        "min_experience": 1
    },
    "Backend Developer": {
        "must_have": ["Node.js", "Express", "SQL", "NoSQL"],
        "nice_to_have": ["GraphQL", "Redis", "Docker"],
        "gpa_cutoff": 3.2,
        "min_experience": 2
    },
    "Full Stack Developer": {
        "must_have": ["JavaScript", "React", "Node.js", "MongoDB"],
        "nice_to_have": ["GraphQL", "Docker", "AWS"],
        "gpa_cutoff": 3.2,
        "min_experience": 2
    },
    "Mobile App Developer": {
        "must_have": ["Flutter", "React Native", "Kotlin", "Swift"],
        "nice_to_have": ["Firebase", "GraphQL", "CI/CD"],
        "gpa_cutoff": 3.2,
        "min_experience": 2
    },
    "Data Analyst": {
        "must_have": ["SQL", "Python", "Excel", "Data Visualization", "ETL", "R"],
        "nice_to_have": ["Tableau", "Power BI", "Statistics", "Google Analytics", "Machine Learning"],
        "gpa_cutoff": 3.0,
        "min_experience": 1
    },
    "Data Scientist": {
        "must_have": ["Python", "Pandas", "Machine Learning"],
        "nice_to_have": ["Deep Learning", "TensorFlow", "PyTorch"],
        "gpa_cutoff": 3.5,
        "min_experience": 2
    },
    "Business Intelligence Analyst": {
        "must_have": ["SQL", "Tableau", "Power BI"],
        "nice_to_have": ["Python", "Excel", "Google Data Studio"],
        "gpa_cutoff": 3.0,
        "min_experience": 1
    },
    "Cloud Engineer": {
        "must_have": ["AWS", "Terraform", "Networking", "Kubernetes", "Linux", "Cloud Security"],
        "nice_to_have": ["Azure", "GCP", "DevOps", "CI/CD", "Ansible"],
        "gpa_cutoff": 3.5,
        "min_experience": 2
    },
    "Site Reliability Engineer (SRE)": {
        "must_have": ["Linux", "Cloud", "Monitoring Tools"],
        "nice_to_have": ["Prometheus", "Grafana", "CI/CD"],
        "gpa_cutoff": 3.3,
        "min_experience": 2
    },
    "IT Support Specialist": {
        "must_have": ["Troubleshooting", "Networking", "Windows/Linux"],
        "nice_to_have": ["AWS", "Cybersecurity Fundamentals"],
        "gpa_cutoff": 2.8,
        "min_experience": 1
    },
    "Cybersecurity Analyst": {
        "must_have": ["Network Security", "SIEM", "Penetration Testing", "Ethical Hacking", "Incident Response"],
        "nice_to_have": ["CISSP", "SOC Analysis", "Cloud Security", "Red Teaming", "Risk Assessment"],
        "gpa_cutoff": 3.3,
        "min_experience": 2
    },
    "Ethical Hacker (Penetration Tester)": {
        "must_have": ["Penetration Testing", "Kali Linux", "Burp Suite"],
        "nice_to_have": ["OSCP", "Bug Bounty Experience"],
        "gpa_cutoff": 3.2,
        "min_experience": 2
    },
    "Security Engineer": {
        "must_have": ["Cloud Security", "IAM", "SOC"],
        "nice_to_have": ["AWS Security", "Zero Trust Security"],
        "gpa_cutoff": 3.4,
        "min_experience": 3
    },
    "Product Manager": {
        "must_have": ["Agile", "Scrum", "Market Research", "Stakeholder Management", "JIRA"],
        "nice_to_have": ["A/B Testing", "SQL", "User Experience", "Lean Methodology"],
        "gpa_cutoff": 3.0,
        "min_experience": 2
    },
    "UI/UX Designer": {
        "must_have": ["Figma", "Sketch", "Wireframing"],
        "nice_to_have": ["Prototyping", "User Testing"],
        "gpa_cutoff": 3.0,
        "min_experience": 1
    },
    "Business Analyst": {
        "must_have": ["Requirements Gathering", "Process Mapping", "Stakeholder Communication", "SQL", "Business Intelligence"],
        "nice_to_have": ["Tableau", "Power BI", "Google Analytics", "R", "Financial Modeling"],
        "gpa_cutoff": 3.2,
        "min_experience": 2
    },
    "IT Project Manager": {
        "must_have": ["Agile", "Project Management", "JIRA"],
        "nice_to_have": ["PMP Certification", "Scrum Master"],
        "gpa_cutoff": 3.2,
        "min_experience": 3
    },
    "Digital Marketing Specialist": {
        "must_have": ["SEO", "Google Ads", "Content Marketing"],
        "nice_to_have": ["Social Media Marketing", "Growth Hacking"],
        "gpa_cutoff": 3.0,
        "min_experience": 1
    },
    "Machine Learning Engineer": {
        "must_have": ["Python", "TensorFlow", "Scikit-Learn", "Deep Learning", "Big Data", "Feature Engineering"],
        "nice_to_have": ["PyTorch", "Data Science", "Cloud ML", "MLOps", "Natural Language Processing"],
        "gpa_cutoff": 3.5,
        "min_experience": 2
    }
}

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
def extract_resume_details(text):
    """
    Extract GPA, experience, and skills from resume text using NLP.
    
    :param text: Resume text as a string.
    :return: Dictionary containing GPA, experience, and skills.
    """
    # Loading spaCy's pre-trained model for named entity recognition
    nlp = spacy.load("en_core_web_sm")

    # Extract GPA using regex
    def extract_gpa(text):
        gpa_patterns = [
            r"gpa\s*[:]?\s*(\d\.\d)",  # Matches "GPA: 3.5" or "GPA 3.5"
            r"grade point average\s*[:]?\s*(\d\.\d)",  # Matches "Grade Point Average: 3.5"
            r"(\d\.\d)\s*gpa"  # Matches "3.5 GPA"
        ]
        for pattern in gpa_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return 0.0  # Default if no GPA is found

    # Extract years of experience using spaCy's NER
    def extract_experience(text):
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "DATE" and "year" in ent.text.lower():
                # Extract numeric value from the entity text
                match = re.search(r"(\d+)", ent.text)
                if match:
                    return int(match.group(1))
        return 0  # Default if no experience is found

    # Extract skills using spaCy's NER and POS tagging
    def extract_skills(text):
        doc = nlp(text)
        skills = set()
        
        # Extract skills from entities (e.g., "Python", "Java")
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "TECH"]:  # Customize labels as needed
                skills.add(ent.text.lower())
        
        # Extract skills from POS tagging (e.g., nouns often represent skills)
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        skills.update([word.lower() for word, pos in tagged if pos in ["NN", "NNS"]])  # Nouns
        
        # Filter out common stopwords
        stop_words = set(stopwords.words('english'))
        skills = [skill for skill in skills if skill not in stop_words]
        
        return list(skills)

    # Extract details
    gpa = extract_gpa(text)
    experience = extract_experience(text)
    skills = extract_skills(text)
    
    return {"gpa": gpa, "experience": experience, "skills": skills}

@app.route("/")
def index():
    return render_template("filters.html", roles=filtering_rules)

@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_files = request.files.getlist("resumes")
    upload_results = []

    for file in uploaded_files:
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            upload_results.append({"filename": filename, "status": "Uploaded successfully!"})
        else:
            upload_results.append({"filename": "Unknown", "status": "Failed to upload"})

    return jsonify({"uploads": upload_results})

@app.route("/filter", methods=["POST"])
def filter_resumes():
    gpa_cutoff = float(request.form.get("gpa_cutoff", 0))
    experience_cutoff = int(request.form.get("experience", 0))
    must_have = [skill.lower() for skill in request.form.getlist("must_have")]

    print("Filtering Resumes...")  # Debugging message
    print(f"Must-Have Skills: {must_have}")
    print(f"GPA Cutoff: {gpa_cutoff}, Experience Cutoff: {experience_cutoff}")

    matching_resumes = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        resume_text = extract_text_from_resume(filepath)
        resume_details = extract_resume_details(resume_text)

        extracted_skills = [skill.lower() for skill in resume_details["skills"]]
        extracted_gpa = resume_details["gpa"]
        extracted_experience = resume_details["experience"]

        print(f"\nProcessing Resume: {filename}")
        print(f"Extracted GPA: {extracted_gpa}, Extracted Experience: {extracted_experience}")
        print(f"Extracted Skills: {extracted_skills}")

        # Check GPA & experience
        meets_gpa = extracted_gpa >= gpa_cutoff
        meets_experience = extracted_experience >= experience_cutoff

        # Fuzzy matching for must-have skills
        has_must_have_skills = all(
            any(fuzz.partial_ratio(skill, extracted_skill) > 80 for extracted_skill in extracted_skills)
            for skill in must_have
        )

        print(f"Meets GPA: {meets_gpa}, Meets Experience: {meets_experience}, Has Must-Have Skills: {has_must_have_skills}")

        if meets_gpa and meets_experience and has_must_have_skills:
            matching_resumes.append(filename)

    print(f"\nMatching Resumes: {matching_resumes}")
    return jsonify({"matching_resumes": matching_resumes})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
