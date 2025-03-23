import sqlite3
import json

# Database connection
conn = sqlite3.connect("knowledge_base.db")
cursor = conn.cursor()

# Create the rules table
cursor.execute('''
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_role TEXT UNIQUE NOT NULL,
    must_have TEXT NOT NULL,
    nice_to_have TEXT,
    gpa_cutoff REAL NOT NULL,
    min_experience INTEGER NOT NULL
)
''')

# Dictionary of job roles and requirements
job_data = {
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
    "Machine Learning Engineer": {
        "must_have": ["Python", "TensorFlow", "Scikit-Learn", "Deep Learning", "Big Data", "Feature Engineering"],
        "nice_to_have": ["PyTorch", "Data Science", "Cloud ML", "MLOps", "Natural Language Processing"],
        "gpa_cutoff": 3.5,
        "min_experience": 2
    }
}

# Insert data into the database
for job, details in job_data.items():
    cursor.execute('''
    INSERT OR IGNORE INTO rules (job_role, must_have, nice_to_have, gpa_cutoff, min_experience)
    VALUES (?, ?, ?, ?, ?)
    ''', (job, json.dumps(details["must_have"]), json.dumps(details["nice_to_have"]), details["gpa_cutoff"], details["min_experience"]))

# Commit and close
conn.commit()
conn.close()

print("Database and table created successfully. Job data inserted!")