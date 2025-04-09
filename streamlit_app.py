import streamlit as st
import os
import shutil
from tempfile import NamedTemporaryFile

from db import SessionLocal, engine
from models import ResumeReview, Role, Base
from parser import extract_resume_text

# Auto-create DB tables
Base.metadata.create_all(bind=engine)

# Streamlit page config
st.set_page_config(page_title="AI Resume Filter", layout="wide")
st.title("📄 AI Resume Filter")

# Sidebar
with st.sidebar:
    st.title("ℹ️ About This App")
    st.markdown("""
    **AI Resume Filter** helps HR teams and hiring managers quickly assess how well a resume matches a job role based on must-have and nice-to-have skills.

    🔍 **Features:**
    - Upload multiple resumes (PDF/DOCX)
    - Select a job role
    - Customize required skills
    - Get match scores and explanations
    - Filter by minimum score

    🐙 [GitHub Repo](https://github.com/lizardcat/ai-resume-filter)
    """)

# DB session
session = SessionLocal()

# Get roles from DB
roles = session.query(Role).all()
role_names = [r.name for r in roles]

if not role_names:
    st.warning("No roles found. Please run `seed.py`.")
    st.stop()

# User selects a role
role_selected = st.selectbox("Select Job Role", role_names)

# Skill selectors
role_obj = session.query(Role).filter_by(name=role_selected).first()
default_must = [s.strip() for s in role_obj.must_have.split(",")]
default_nice = [s.strip() for s in role_obj.nice_to_have.split(",")]

selected_must = st.multiselect("Must-Have Skills", options=default_must, default=default_must)
selected_nice = st.multiselect("Nice-To-Have Skills", options=default_nice, default=default_nice)

# Upload resumes
uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True)
min_score = st.slider("Minimum Match Score (%)", 0, 100, 50, 5)

# Skill matcher
def skill_match(text, skills):
    text_lower = text.lower()
    return [s for s in skills if s.lower() in text_lower]

# Run filter
if st.button("Run Resume Filter"):
    if not uploaded_files:
        st.error("Upload at least one resume.")
    elif not selected_must:
        st.error("Select at least one must-have skill.")
    else:
        results = []

        for file in uploaded_files:
            ext = os.path.splitext(file.name)[-1].lower()
            with NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                shutil.copyfileobj(file, temp_file)
                temp_path = temp_file.name

            text = extract_resume_text(temp_path)
            os.unlink(temp_path)

            if not text:
                continue

            matched_must = skill_match(text, selected_must)
            matched_nice = skill_match(text, selected_nice)
            score = len(matched_must) / len(selected_must) if selected_must else 0

            explanation = (
                f"{file.name} matches {len(matched_must)} of {len(selected_must)} must-have skills "
                f"({', '.join(matched_must)}) and these nice-to-have skills: {', '.join(matched_nice)}."
            )

            session.add(ResumeReview(
                resume_text=text,
                role=role_selected,
                score=score,
                explanation=explanation,
                filename=file.name
            ))
            session.commit()

            results.append((file.name, score, explanation, text[:1000]))

        # Filter + show
        filtered = [r for r in results if r[1] * 100 >= min_score]

        st.subheader("🎯 Results")
        if not filtered:
            st.warning("No resumes matched your filters.")
        for name, score, explanation, preview in sorted(filtered, key=lambda x: x[1], reverse=True):
            st.markdown(f"**{name} — {round(score * 100)}% match**")
            st.write(explanation)
            with st.expander("Preview Resume Text"):
                st.text(preview + "...")
