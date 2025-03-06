from flask import Flask
from models import db, JobRole  # Import directly from models.py
from app import app  # Import after models are defined


def seed_database():
    with app.app_context():  # Ensure database operations run within Flask's context
        db.create_all()

        roles = [
            JobRole("Software Engineer", ["Java", "Spring Boot", "Git", "REST APIs"], ["Docker", "CI/CD"], 3.2, 2),
            JobRole("Frontend Developer", ["HTML", "CSS", "JavaScript", "React"], ["Vue.js", "Figma"], 3.0, 1),
            JobRole("Backend Developer", ["Node.js", "Express", "SQL", "NoSQL"], ["GraphQL", "Redis", "Docker"], 3.2, 2),
            JobRole("Full Stack Developer", ["JavaScript", "React", "Node.js", "MongoDB"], ["GraphQL", "Docker", "AWS"], 3.2, 2),
            JobRole("Mobile App Developer", ["Flutter", "React Native", "Kotlin", "Swift"], ["Firebase", "GraphQL", "CI/CD"], 3.2, 2),
            JobRole("Data Analyst", ["SQL", "Python", "Excel", "Data Visualization"], ["Power BI", "ETL"], 3.0, 1),
            JobRole("Data Scientist", ["Python", "Pandas", "Machine Learning"], ["Deep Learning", "TensorFlow", "PyTorch"], 3.5, 2),
            JobRole("Business Intelligence Analyst", ["SQL", "Tableau", "Power BI"], ["Python", "Google Data Studio"], 3.0, 1),
            JobRole("Cloud Engineer", ["AWS", "Terraform", "Kubernetes"], ["Azure", "GCP"], 3.5, 2),
            JobRole("Site Reliability Engineer (SRE)", ["Linux", "Cloud", "Monitoring Tools"], ["Prometheus", "Grafana", "CI/CD"], 3.3, 2),
            JobRole("IT Support Specialist", ["Troubleshooting", "Networking", "Windows/Linux"], ["AWS", "Cybersecurity Fundamentals"], 2.8, 1),
            JobRole("Cybersecurity Analyst", ["Network Security", "SIEM", "Penetration Testing"], ["CISSP", "Cloud Security"], 3.3, 2),
            JobRole("Ethical Hacker (Penetration Tester)", ["Penetration Testing", "Kali Linux", "Burp Suite"], ["OSCP", "Bug Bounty"], 3.2, 2),
            JobRole("Security Engineer", ["Cloud Security", "IAM", "SOC"], ["AWS Security", "Zero Trust Security"], 3.4, 3),
            JobRole("Product Manager", ["Agile", "Scrum", "Market Research"], ["A/B Testing", "User Experience"], 3.0, 2),
            JobRole("UI/UX Designer", ["Figma", "Sketch", "Wireframing"], ["Prototyping", "User Testing"], 3.0, 1),
            JobRole("Business Analyst", ["Requirements Gathering", "Process Mapping"], ["Tableau", "Google Analytics"], 3.2, 2),
            JobRole("IT Project Manager", ["Agile", "Project Management", "JIRA"], ["PMP Certification", "Scrum Master"], 3.2, 3),
            JobRole("Digital Marketing Specialist", ["SEO", "Google Ads", "Content Marketing"], ["Social Media Marketing", "Growth Hacking"], 3.0, 1),
            JobRole("Machine Learning Engineer", ["Python", "TensorFlow", "Scikit-Learn"], ["PyTorch", "Cloud ML"], 3.5, 2),
            JobRole("DevOps Engineer", ["Docker", "Kubernetes", "Jenkins"], ["AWS", "Terraform", "Ansible"], 3.2, 2),
            JobRole("Database Administrator", ["SQL", "Oracle", "MySQL"], ["MongoDB", "PostgreSQL"], 3.2, 2),
            JobRole("Embedded Systems Engineer", ["C", "C++", "RTOS"], ["FPGA", "Microcontrollers"], 3.3, 2),
            JobRole("Game Developer", ["Unity", "Unreal Engine", "C#"], ["3D Modeling", "Game AI"], 3.0, 2),
            JobRole("Blockchain Developer", ["Solidity", "Ethereum", "Smart Contracts"], ["Hyperledger", "Cryptography"], 3.4, 2),
        ]

        for role in roles:
            existing_role = JobRole.query.filter_by(title=role.title).first()
            if not existing_role:
                db.session.add(role)

        db.session.commit()
        print("✅ Database Seeded with 20+ Job Roles!")

if __name__ == "__main__":
    seed_database()
