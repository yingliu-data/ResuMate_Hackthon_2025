from flask import Flask, request, redirect, session
import os
from dotenv import load_dotenv
import requests
from github import Github

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
        <h1>GitHub Project Analyzer</h1>
        <a href="/login/github">
            <button style="padding: 10px 20px; font-size: 16px;">
                Login with GitHub
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
    # resume_summary = f"{user.name or user.login} is a software developer skilled in {', '.join(languages) or 'various technologies'}."
    resume_summary = " They have created multiple projects, including:\n"

    # Print résumé summary in console
    print("\n📌 GitHub Resume")
    print("=" * 40)
    print(resume_summary)
    print("\n".join(repo_summaries))

    # Return résumé summary as a webpage
    formatted_resume = f"<h2>GitHub Resume for {user.name or user.login}</h2><p>{resume_summary}</p><ul>"
    for summary in repo_summaries:
        formatted_resume += f"<li>{summary}</li>"
    formatted_resume += "</ul>"

    return formatted_resume


if __name__ == '__main__':
    # Ensure environment variables are loaded
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("GitHub OAuth credentials not found. Check your .env file.")

    app.run(debug=True, port=5000)
