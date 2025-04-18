# scoring.py

from sentence_transformers import SentenceTransformer, util

# Load the model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(job_description, resume_text):
    """
    Calculate semantic similarity between job description and resume text.
    Returns a percentage score.
    """
    if not job_description or not resume_text:
        return 0.0

    job_embed = model.encode(job_description, convert_to_tensor=True)
    resume_embed = model.encode(resume_text, convert_to_tensor=True)
    similarity = util.cos_sim(job_embed, resume_embed).item()
    return round(similarity * 100, 2)
 
 