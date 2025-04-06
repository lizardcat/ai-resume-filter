from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ResumeReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_text = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(120))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    must_have = db.Column(db.Text, nullable=False)
    nice_to_have = db.Column(db.Text, nullable=False)