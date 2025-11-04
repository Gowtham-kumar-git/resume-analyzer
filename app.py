from flask import Flask, render_template, request
import os
from utils.resume_parser import extract_text, analyze_resume

app = Flask(__name__)

# Create an uploads folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the uploaded file and job description
        file = request.files.get('resume')
        job_desc = request.form.get('job_desc', '')

        if not file:
            return render_template('index.html', results={"error": "No file uploaded."})

        # Save uploaded file to 'uploads' folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extract text and analyze resume
        resume_text = extract_text(filepath)
        results = analyze_resume(resume_text, job_desc)

        return render_template('index.html', results=results)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', results={"error": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    # Allow external access (for Docker/AWS)
    app.run(host='0.0.0.0', port=5000)
