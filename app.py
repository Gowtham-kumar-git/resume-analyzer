from flask import Flask, render_template, request
import docx2txt
import pdfplumber
import os
from textblob import TextBlob
import re
from collections import Counter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_file(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.endswith('.docx'):
        text = docx2txt.process(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    return text.strip()

def analyze_resume(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)

    keywords = ['python', 'java', 'flask', 'sql', 'machine learning', 'aws', 'git', 'html', 'css', 'javascript']
    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    missing_keywords = [kw for kw in keywords if kw.lower() not in text.lower()]

    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.2:
        sentiment_result = "Positive"
    elif sentiment < -0.2:
        sentiment_result = "Negative"
    else:
        sentiment_result = "Neutral"

    most_common_words = [w for w, _ in Counter(words).most_common(5)]

    # Simple readability metric
    sentences = re.split(r'[.!?]', text)
    avg_sentence_length = word_count / max(len(sentences), 1)
    readability = round(206.835 - (1.015 * avg_sentence_length) - (84.6 * (word_count / (len(text.split()) + 1))), 2)

    summary = f"This resume has {word_count} words, includes {len(found_keywords)} key skills, and is written with a {sentiment_result.lower()} tone."

    return {
        'word_count': word_count,
        'found_keywords': found_keywords,
        'missing_keywords': missing_keywords,
        'sentiment': sentiment_result,
        'most_common_words': most_common_words,
        'readability': readability,
        'summary': summary
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('resume')
    if not file:
        return render_template('index.html', error="Please upload a resume file.")
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    text = extract_text_from_file(file_path)
    if not text:
        return render_template('index.html', error="Could not extract text from the file.")
    
    result = analyze_resume(text)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
