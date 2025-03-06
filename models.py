from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JobRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    must_have = db.Column(db.Text, nullable=False)  # Stored as a comma-separated string
    nice_to_have = db.Column(db.Text, nullable=True)  # Optional
    gpa_cutoff = db.Column(db.Float, nullable=False)
    min_experience = db.Column(db.Integer, nullable=False)

    def __init__(self, title, must_have, nice_to_have, gpa_cutoff, min_experience):
        self.title = title
        self.must_have = ",".join(must_have)  # Convert list to comma-separated string
        self.nice_to_have = ",".join(nice_to_have) if nice_to_have else ""
        self.gpa_cutoff = gpa_cutoff
        self.min_experience = min_experience

    def to_dict(self):
        return {
            "title": self.title,
            "must_have": self.must_have.split(",") if self.must_have else [],
            "nice_to_have": self.nice_to_have.split(",") if self.nice_to_have else [],
            "gpa_cutoff": self.gpa_cutoff,
            "min_experience": self.min_experience
        }

