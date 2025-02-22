from flask import Flask, request, redirect, session, jsonify
import os
from dotenv import load_dotenv
import requests
from github import Github
import json
import fitz  # PyMuPDF for PDF extraction
import pdfplumber

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# GitHub OAuth credentials
CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
CALLBACK_URL = "http://127.0.0.1:5000/github/callback"


@app.route('/')
def index():
    return '''
        <h1>AI Resume Builder</h1>
        <a href="/login/github">
            <button style="padding: 10px 20px; font-size: 16px;">
                Login with GitHub
            </button>
        </a><br><br>
        <form action="/upload_pdf" method="POST" enctype="multipart/form-data">
            <label for="pdf_file">Upload PDF Resume:</label>
            <input type="file" name="pdf_file" accept="application/pdf" required>
            <button type="submit">Upload PDF</button>
        </form>
    '''


@app.route('/login/github')
def github_login():
    github_auth_url = (
        f'https://github.com/login/oauth/authorize'
        f'?client_id={CLIENT_ID}'
        f'&redirect_uri={CALLBACK_URL}'
        f'&scope=repo'
    )
    return redirect(github_auth_url)


@app.route('/github/callback')
def github_callback():
    code = request.args.get('code')

    response = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': CALLBACK_URL
        },
        headers={'Accept': 'application/json'}
    )

    access_token = response.json().get('access_token')

    if access_token:
        session['access_token'] = access_token
        return redirect('/repos')
    return 'Failed to get access token', 400


@app.route('/repos')
def list_repos():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/')

    g = Github(access_token)
    user = g.get_user()

    repo_summaries = []
    languages = set()

    for repo in user.get_repos():
        if not repo.fork:  # Only include original projects
            description = repo.description or "No description available"
            language = repo.language or "Not specified"
            stars = repo.stargazers_count

            # Track languages used
            if repo.language:
                languages.add(repo.language)

            # Generate résumé-style summary
            summary = f"- **{repo.name}** ({language}): {description} [⭐ {stars} stars]"
            repo_summaries.append(summary)

    # Generate a high-level resume summary
    resume_summary = "They have created multiple projects, including:\n"

    # Return résumé summary as a webpage
    formatted_resume = f"<h2>GitHub Resume for {user.name or user.login}</h2><p>{resume_summary}</p><ul>"
    for summary in repo_summaries:
        formatted_resume += f"<li>{summary}</li>"
    formatted_resume += "</ul>"

    return formatted_resume


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return 'No file uploaded', 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return 'No selected file', 400

    # Save the PDF temporarily to the server
    pdf_file_path = os.path.join("uploads", pdf_file.filename)
    pdf_file.save(pdf_file_path)

    # Extract text from PDF
    pdf_text = extract_pdf_text(pdf_file_path)

    # Store the raw text for LLM processing (as a whole string)
    save_pdf_text_for_llm(pdf_text)

    # Clean up the uploaded PDF file (optional)
    os.remove(pdf_file_path)

    return "PDF text extracted and saved successfully!"


def extract_pdf_text(pdf_file_path):
    # Extract text using PyMuPDF (fitz)
    doc = fitz.open(pdf_file_path)
    pdf_text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pdf_text += page.get_text()
    return pdf_text


def save_pdf_text_for_llm(text):
    # You can save the raw text in a file for future processing
    with open("resume_text.txt", "w") as file:
        file.write(text)

    # Alternatively, store it in a structured way (JSON) for easier handling
    resume_data = {
        "raw_text": text
    }
    with open("resume_data.json", "w") as json_file:
        json.dump(resume_data, json_file)

    print("Text saved for LLM processing.")


if __name__ == '__main__':
    # Ensure environment variables are loaded
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("GitHub OAuth credentials not found. Check your .env file.")

    # Ensure the 'uploads' folder exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    app.run(debug=True, port=5000)
