from textblob import TextBlob
import PyPDF2
import re

def extract_text(filepath):
    text = ""
    if filepath.lower().endswith(".pdf"):
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    else:
        text = open(filepath, "r", encoding="utf-8", errors="ignore").read()
    return text

def analyze_resume(text, job_desc=""):
    blob = TextBlob(text)
    word_count = len(blob.words)
    summary = " ".join(str(s) for s in blob.sentences[:3]) if len(blob.sentences) > 0 else "No summary available."

    keywords_found, missing_keywords = [], []
    if job_desc:
        job_words = re.findall(r'\b[a-zA-Z]{4,}\b', job_desc.lower())
        for word in set(job_words):
            if word in text.lower():
                keywords_found.append(word)
            else:
                missing_keywords.append(word)

    readability = estimate_readability(text)

    return {
        "word_count": word_count,
        "keywords_found": ", ".join(keywords_found[:15]) or "None",
        "missing_keywords": ", ".join(missing_keywords[:15]) or "None",
        "readability": f"{readability:.2f}/100 (higher is easier to read)",
        "summary": summary
    }

def estimate_readability(text):
    words = len(re.findall(r'\w+', text))
    sentences = len(re.findall(r'[.!?]', text))
    syllables = len(re.findall(r'[aeiouyAEIOUY]', text))
    if sentences == 0 or words == 0:
        return 0
    score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return max(0, min(100, score))
