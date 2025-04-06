# AI Resume Screener

This is an AI-powered resume screening system built using Python, Flask, and SQLite. It uses sentence-transformers to compute semantic similarity between resumes and job descriptions, and leverages a local LLaMA 2 model (via [Ollama](https://ollama.com)) to generate natural language explanations.

## Features
- Upload one or more resumes in PDF or DOCX format
- Enter a job description to compare against
- Automatically scores each resume based on semantic similarity
- Generates explanations using a locally running LLaMA 2 model
- Stores all results in a local SQLite database
- Filter results by match score threshold
- Responsive UI with Bootstrap styling

## Requirements
- Python 3.9+
- Ollama installed and running locally

### Python Dependencies
Install all required dependencies:

```bash
pip install flask flask_sqlalchemy sentence-transformers python-docx pymupdf python-dotenv requests
```

## Setup
1. Clone the repo
2. Make sure you have [Ollama](https://ollama.com) installed
3. Pull and start the LLaMA 2 model:

```bash
ollama run llama2
```

4. Run the app:

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Notes
- Resume match results are stored in `reviews.db`
- Uploaded resumes go to the `uploads/` folder
- Make sure Ollama is running and the LLaMA 2 model is loaded before using the app
- The `.env` file is no longer required for this version since OpenAI is not used