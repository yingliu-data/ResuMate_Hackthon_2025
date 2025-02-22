from flask import Flask, request, redirect, session, jsonify
import os
from dotenv import load_dotenv
import requests
from github import Github
import json
import fitz  # PyMuPDF for PDF extraction
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# GitHub OAuth credentials
CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
CALLBACK_URL = "http://127.0.0.1:5000/github/callback"

# Ensure 'uploads' folder exists
UPLOADS_FOLDER = "uploads"
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)


@app.route('/')
def index():
    github_message = "<p style='color:green;'>GitHub information received successfully!</p>" if session.get('github_connected') else ""
    pdf_message = "<p style='color:green;'>PDF uploaded and processed successfully!</p>" if session.get('pdf_uploaded') else ""

    return f'''
        <h1>AI Resume Builder</h1>
        {github_message}
        {pdf_message}
        <a href="/login/github">
            <button style="padding: 10px 20px; font-size: 16px;">
                Login with GitHub
            </button>
        </a><br><br>
        <form action="/upload_pdf" method="POST" enctype="multipart/form-data">
            <label for="pdf_file">Upload PDF Resume:</label>
            <input type="file" name="pdf_file" accept="application/pdf">
            <button type="submit">Upload PDF</button>
        </form>
        <br>
        <a href="/extract_text">
            <button style="padding: 10px 20px; font-size: 16px;">
                Extract & Send Data
            </button>
        </a>
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
        session['github_connected'] = True  # Store a flag to confirm login
        return redirect('/')
    return 'Failed to get access token', 400


def fetch_github_resume():
    """Fetch GitHub repositories and return a formatted résumé-style text."""
    access_token = session.get('access_token')
    if not access_token:
        print("GitHub not connected.")
        return None

    g = Github(access_token)
    user = g.get_user()

    repo_summaries = []
    for repo in user.get_repos():
        if not repo.fork:
            description = repo.description or "No description available"
            language = repo.language or "Not specified"
            stars = repo.stargazers_count
            summary = f"- {repo.name} ({language}): {description} [⭐ {stars} stars]"
            repo_summaries.append(summary)

    if not repo_summaries:
        return None

    github_resume_text = f"GitHub Profile: {user.name or user.login}\n\n"
    github_resume_text += "Projects:\n" + "\n".join(repo_summaries)

    return github_resume_text


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """Uploads a PDF, extracts and saves its text for later retrieval."""
    if 'pdf_file' not in request.files:
        return 'No file uploaded', 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return 'No selected file', 400

    pdf_file_path = os.path.join(UPLOADS_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_file_path)

    pdf_text = extract_pdf_text(pdf_file_path)
    cleaned_text = clean_text(pdf_text)

    save_pdf_text_for_llm(cleaned_text)

    session['pdf_uploaded'] = True  # Store a flag to confirm upload

    os.remove(pdf_file_path)  # Remove uploaded file after processing

    return redirect('/')


def extract_pdf_text(pdf_file_path):
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_file_path)
    pdf_text = ""
    for page in doc:
        pdf_text += page.get_text() + "\n"
    return pdf_text


def clean_text(text):
    """Cleans extracted text for better readability."""
    text = text.replace("\u00a0", " ").replace("�", "").strip()
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = text.replace("•", "-").replace("�", "-")
    return text


def save_pdf_text_for_llm(text):
    """Saves cleaned PDF text for retrieval."""
    with open(os.path.join(UPLOADS_FOLDER, "resume_text_cleaned.txt"), "w", encoding="utf-8") as file:
        file.write(text)
    with open(os.path.join(UPLOADS_FOLDER, "resume_data_cleaned.json"), "w", encoding="utf-8") as json_file:
        json.dump({"cleaned_text": text}, json_file, indent=4)


def get_pdf_text():
    """Retrieves previously saved PDF text."""
    pdf_file_path = os.path.join(UPLOADS_FOLDER, "resume_text_cleaned.txt")
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, "r", encoding="utf-8") as file:
            return file.read()
    print("No PDF text found.")
    return None


@app.route('/extract_text', methods=['GET'])
def extract_text():
    """Returns extracted text from GitHub and/or PDF as JSON."""
    github_resume = fetch_github_resume()
    pdf_resume = get_pdf_text()

    combined_data = {
        "github_text": github_resume if github_resume else "No GitHub data found.",
        "pdf_text": pdf_resume if pdf_resume else "No PDF data found."
    }

    # Save the combined data to a JSON file for future retrieval
    save_combined_data(combined_data)

    return jsonify(combined_data)


def save_combined_data(data):
    """Saves both GitHub and PDF data to a JSON file."""
    file_path = os.path.join(UPLOADS_FOLDER, "combined_data.json")
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Saved combined data to {file_path}")
    except Exception as e:
        print(f"Error saving combined data: {e}")


def get_combined_data():
    """Retrieves the combined GitHub and PDF data from the saved file."""
    file_path = os.path.join(UPLOADS_FOLDER, "combined_data.json")
    if not os.path.exists(file_path):
        print("No combined data file found.")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Error reading combined data file: {e}")
        return None


if __name__ == '__main__':
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("GitHub OAuth credentials missing. Check your .env file.")

    app.run(debug=True, port=5000)
