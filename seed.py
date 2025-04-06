
from models import db, Role
from app import app

role_data = {
    "Software Engineer": {
        "must_have": ["Java", "Spring Boot", "Git", "REST APIs", "Agile", "Unit Testing"],
        "nice_to_have": ["Docker", "Kubernetes", "Microservices", "CI/CD", "GraphQL", "React"]
    },
    "Frontend Developer": {
        "must_have": ["HTML", "CSS", "JavaScript", "React"],
        "nice_to_have": ["Vue.js", "Angular", "Figma"]
    },
    "Backend Developer": {
        "must_have": ["Node.js", "Express", "SQL", "NoSQL"],
        "nice_to_have": ["GraphQL", "Redis", "Docker"]
    },
    "Full Stack Developer": {
        "must_have": ["JavaScript", "React", "Node.js", "MongoDB"],
        "nice_to_have": ["GraphQL", "Docker", "AWS"]
    },
    "Mobile App Developer": {
        "must_have": ["Flutter", "React Native", "Kotlin", "Swift"],
        "nice_to_have": ["Firebase", "GraphQL", "CI/CD"]
    },
    "Data Analyst": {
        "must_have": ["SQL", "Python", "Excel", "Data Visualization", "ETL", "R"],
        "nice_to_have": ["Tableau", "Power BI", "Statistics", "Google Analytics", "Machine Learning"]
    },
    "Data Scientist": {
        "must_have": ["Python", "Pandas", "Machine Learning"],
        "nice_to_have": ["Deep Learning", "TensorFlow", "PyTorch"]
    },
    "Business Intelligence Analyst": {
        "must_have": ["SQL", "Tableau", "Power BI"],
        "nice_to_have": ["Python", "Excel", "Google Data Studio"]
    },
    "Cloud Engineer": {
        "must_have": ["AWS", "Terraform", "Networking", "Kubernetes", "Linux", "Cloud Security"],
        "nice_to_have": ["Azure", "GCP", "DevOps", "CI/CD", "Ansible"]
    },
    "Site Reliability Engineer (SRE)": {
        "must_have": ["Linux", "Cloud", "Monitoring Tools"],
        "nice_to_have": ["Prometheus", "Grafana", "CI/CD"]
    },
    "IT Support Specialist": {
        "must_have": ["Troubleshooting", "Networking", "Windows/Linux"],
        "nice_to_have": ["AWS", "Cybersecurity Fundamentals"]
    },
    "Cybersecurity Analyst": {
        "must_have": ["Network Security", "SIEM", "Penetration Testing", "Ethical Hacking", "Incident Response"],
        "nice_to_have": ["CISSP", "SOC Analysis", "Cloud Security", "Red Teaming", "Risk Assessment"]
    },
    "Ethical Hacker (Penetration Tester)": {
        "must_have": ["Penetration Testing", "Kali Linux", "Burp Suite"],
        "nice_to_have": ["OSCP", "Bug Bounty Experience"]
    },
    "Security Engineer": {
        "must_have": ["Cloud Security", "IAM", "SOC"],
        "nice_to_have": ["AWS Security", "Zero Trust Security"]
    },
    "Product Manager": {
        "must_have": ["Agile", "Scrum", "Market Research", "Stakeholder Management", "JIRA"],
        "nice_to_have": ["A/B Testing", "SQL", "User Experience", "Lean Methodology"]
    },
    "UI/UX Designer": {
        "must_have": ["Figma", "Sketch", "Wireframing"],
        "nice_to_have": ["Prototyping", "User Testing"]
    },
    "Business Analyst": {
        "must_have": ["Requirements Gathering", "Process Mapping", "Stakeholder Communication", "SQL", "Business Intelligence"],
        "nice_to_have": ["Tableau", "Power BI", "Google Analytics", "R", "Financial Modeling"]
    },
    "IT Project Manager": {
        "must_have": ["Agile", "Project Management", "JIRA"],
        "nice_to_have": ["PMP Certification", "Scrum Master"]
    },
    "Digital Marketing Specialist": {
        "must_have": ["SEO", "Google Ads", "Content Marketing"],
        "nice_to_have": ["Social Media Marketing", "Growth Hacking"]
    },
    "Machine Learning Engineer": {
        "must_have": ["Python", "TensorFlow", "Scikit-Learn", "Deep Learning", "Big Data", "Feature Engineering"],
        "nice_to_have": ["PyTorch", "Data Science", "Cloud ML", "MLOps", "Natural Language Processing"]
    }
}

with app.app_context():
    db.drop_all()
    db.create_all()
    for role_name, skills in role_data.items():
        role = Role(
            name=role_name,
            must_have=",".join(skills["must_have"]),
            nice_to_have=",".join(skills["nice_to_have"])
        )
        db.session.add(role)
    db.session.commit()
    print("✅ Roles seeded successfully.")
