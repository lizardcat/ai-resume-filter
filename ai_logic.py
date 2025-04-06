# ai_logic.py (LLaMA version using Ollama)
from sentence_transformers import SentenceTransformer, util
import requests
from models import ResumeReview, db

# Load sentence transformer for semantic similarity
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def compute_match_score(resume_text, job_description):
    """
    Uses sentence-transformers to compute cosine similarity between resume and job description.
    """
    resume_embedding = embedder.encode(resume_text, convert_to_tensor=True)
    job_embedding = embedder.encode(job_description, convert_to_tensor=True)
    score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
    return score

def generate_reasoning(resume_text, job_description):
    """
    Calls a locally running LLaMA model via Ollama to generate a match explanation.
    Ollama must be running locally with `ollama run llama2` beforehand.
    """
    prompt = f"""
You are an AI HR assistant. Given the following job description and resume, determine how well the resume fits the job and explain why.

Job Description:
{job_description}

Resume:
{resume_text}

Respond with a clear summary of how well this candidate fits the role and list key points for the decision.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt},
        stream=True
    )

    result = ""
    for line in response.iter_lines():
        if line:
            try:
                part = eval(line.decode("utf-8"))
                result += part.get("response", "")
            except Exception:
                continue

    return result.strip()

def save_review(resume, job, score, explanation):
    """
    Save the resume review result into the SQLite database.
    """
    review = ResumeReview(
        resume_text=resume,
        job_description=job,
        score=score,
        explanation=explanation
    )
    db.session.add(review)
    db.session.commit()
