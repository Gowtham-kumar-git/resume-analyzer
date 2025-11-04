FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🧠 Download NLTK and TextBlob data
RUN python -m nltk.downloader punkt punkt_tab stopwords wordnet \
    && python -m textblob.download_corpora

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
