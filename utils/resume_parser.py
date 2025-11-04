import re
from textblob import TextBlob
from PyPDF2 import PdfReader

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return text

def analyze_resume(text, job_desc=""):
    skills = re.findall(r"\b(Python|Java|C\+\+|SQL|HTML|CSS|JavaScript|AWS|Docker|Flask|TensorFlow)\b", text, re.I)
    education = re.findall(r"\b(B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|B\.?E|M\.?E|Bachelor|Master|Ph\.?D)\b", text, re.I)
    exp_years = re.findall(r"(\d+)\s+years?", text)
    exp = max([int(x) for x in exp_years], default=0)

    # Job match score
    match_score = 0
    if job_desc:
        resume_blob = TextBlob(text.lower())
        job_blob = TextBlob(job_desc.lower())
        common_words = len(set(resume_blob.words) & set(job_blob.words))
        match_score = round(common_words / (len(job_blob.words) + 1) * 100, 2)

    return {
        "skills": sorted(set(skills)),
        "education": sorted(set(education)),
        "experience": exp,
        "match_score": match_score
    }
