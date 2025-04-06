from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from models import db, ResumeReview, Role
from parser import extract_resume_text
import spacy
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db.init_app(app)
nlp = spacy.load("en_core_web_sm")

def skill_match(resume_text, required_skills):
    doc = nlp(resume_text.lower())
    tokens = set([token.text for token in doc if not token.is_stop])
    return [skill for skill in required_skills if skill.lower() in tokens]

@app.route('/', methods=['GET', 'POST'])
def index():
    roles = Role.query.all()

    if request.method == 'POST':
        files = request.files.getlist('resumeFiles')
        selected_role = request.form.get('role')
        selected_must_have = request.form.getlist('selected_must_have')
        selected_nice_to_have = request.form.getlist('selected_nice_to_have')

        role = Role.query.filter_by(name=selected_role).first()

        # Use selected skills or fall back to the full role defaults
        must_have_skills = selected_must_have if selected_must_have else role.must_have.split(",")
        nice_to_have_skills = selected_nice_to_have if selected_nice_to_have else role.nice_to_have.split(",")

        reviews = []
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            resume_text = extract_resume_text(file)
            if not resume_text:
                continue

            matched_must = skill_match(resume_text, must_have_skills)
            matched_nice = skill_match(resume_text, nice_to_have_skills)

            score = len(matched_must) / len(must_have_skills) if must_have_skills else 0
            explanation = (
                f"{filename} meets {len(matched_must)} of {len(must_have_skills)} must-have skills"
                f" ({', '.join(matched_must)}) and also has these nice-to-have skills: {', '.join(matched_nice)}."
            )

            review = ResumeReview(
                resume_text=resume_text,
                role=selected_role,
                score=score,
                explanation=explanation,
                filename=filename
            )
            db.session.add(review)
            reviews.append(review)

        db.session.commit()
        return render_template('results.html', reviews=reviews)

    # Prepare role data for frontend JS
    role_data = {
        role.name: {
            "must_have": [skill.strip() for skill in role.must_have.split(",")],
            "nice_to_have": [skill.strip() for skill in role.nice_to_have.split(",")]
        } for role in roles
    }
    return render_template('index.html', roles=roles, role_data=role_data)


@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
