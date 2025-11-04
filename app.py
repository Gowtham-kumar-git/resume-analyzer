from flask import Flask, render_template, request
import os
from utils.resume_parser import extract_text, analyze_resume

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    job_desc = request.form.get('job_desc', '')

    if not file:
        return "No file uploaded", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    resume_text = extract_text(filepath)
    results = analyze_resume(resume_text, job_desc)

    return render_template('index.html', results=results, job_desc=job_desc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
