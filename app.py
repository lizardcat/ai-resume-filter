import streamlit as st
from parser import extract_resume_text
import spacy
from db import SessionLocal
from models import Role
from sqlalchemy import select
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Skill matching function
def skill_match(resume_text, required_skills):
    doc = nlp(resume_text.lower())
    tokens = set([token.text for token in doc if not token.is_stop])
    return [skill for skill in required_skills if skill.lower() in tokens]

# Streamlit app
st.title("AI Resume Filter")
st.subheader("Streamline your hiring process with AI-powered resume screening.")

# Sidebar description
st.sidebar.title("About the App")
st.sidebar.info(
    """
    **AI Resume Filter** helps recruiters and hiring managers streamline the resume screening process. 
    Upload resumes in PDF or DOCX format, select a job role, and the app will:
    
    - Match resumes against must-have and nice-to-have skills for the selected role.
    - Provide a compatibility score for each resume.
    - Highlight matched skills for better decision-making.
    
    This tool leverages **Natural Language Processing (NLP)** and a database of predefined roles and skills.
    """
)

# Database session
db = next(get_db())

# Fetch roles from the database
roles = db.execute(select(Role)).scalars().all()
role_names = [role.name for role in roles]

# Role selection
st.markdown("### Select a Job Role")
selected_role = st.selectbox("Select Job Role", ["-- Select a role --"] + role_names)

if selected_role and selected_role != "-- Select a role --":
    # Fetch role details
    role = db.execute(select(Role).where(Role.name == selected_role)).scalar_one()
    must_have_skills = role.must_have.split(",")
    nice_to_have_skills = role.nice_to_have.split(",")

    # Display skills for selection
    st.markdown("### Customize Skills")
    col1, col2 = st.columns(2)
    with col1:
        selected_must_have = st.multiselect("Must-Have Skills", must_have_skills, default=must_have_skills)
    with col2:
        selected_nice_to_have = st.multiselect("Nice-to-Have Skills", nice_to_have_skills, default=nice_to_have_skills)

    # File upload
    st.markdown("### Upload Resumes")
    uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("Filter Resumes"):
        if uploaded_files:
            reviews = []
            progress_bar = st.progress(0)
            for i, file in enumerate(uploaded_files):
                resume_text = extract_resume_text(file)
                if not resume_text:
                    st.warning(f"Could not parse {file.name}. Skipping.")
                    continue

                matched_must = skill_match(resume_text, selected_must_have)
                matched_nice = skill_match(resume_text, selected_nice_to_have)

                score = len(matched_must) / len(selected_must_have) if selected_must_have else 0
                explanation = (
                    f"{file.name} meets {len(matched_must)} of {len(selected_must_have)} must-have skills"
                    f" ({', '.join(matched_must)}) and also has these nice-to-have skills: {', '.join(matched_nice)}."
                )

                reviews.append({
                    "filename": file.name,
                    "score": round(score * 100, 2),
                    "explanation": explanation
                })

                progress_bar.progress((i + 1) / len(uploaded_files))

            # Display results
            st.subheader("Screening Results")
            for review in reviews:
                st.write(f"**{review['filename']}**")
                st.write(f"Score: {review['score']}%")
                st.write(f"Explanation: {review['explanation']}")
                st.write("---")
        else:
            st.warning("Please upload at least one resume.")
else:
    st.info("Please select a job role to begin.")

# Footer
st.markdown("---")
st.markdown("**Developed by Raza Shirlie Paul Hamisi** | Powered by Streamlit and spaCy")