import os
import random
import base64
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # secret for session

# Load config from .env
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = os.getenv("REPO_URL")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
CDN_URL = os.getenv("CDN_URL")

APP_USERNAME = os.getenv("APP_USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# ------------------ Middleware: Require Login ------------------

@app.before_request
def require_login():
    if request.endpoint not in ['login', 'static'] and 'logged_in' not in session:
        return redirect(url_for('login'))

# ------------------ Login Route ------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == APP_USERNAME and password == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error="Username atau password salah.")
    return render_template('login.html')

# ------------------ Logout Route ------------------

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# ------------------ Index (Upload Page) ------------------

@app.route('/')
def index():
    # generate simple captcha question
    a, b = random.randint(1, 9), random.randint(1, 9)
    session['captcha_answer'] = a + b
    return render_template('index.html', captcha=f"{a} + {b}")

# ------------------ Upload Route ------------------

@app.route('/upload', methods=['POST'])
def upload():
    # Validate captcha
    captcha_input = request.form.get('captcha')
    if not captcha_input or int(captcha_input) != session.get('captcha_answer', -1):
        return jsonify({"error": "Captcha salah."}), 400

    uploaded_files = request.files.getlist("file")
    urls = []

    for file in uploaded_files:
        if file.filename == "" or not file.mimetype.startswith("image/"):
            continue

        content = file.read()
        b64_content = base64.b64encode(content).decode("utf-8")
        github_api = f"{REPO_URL}/contents/{UPLOAD_FOLDER}/{file.filename}"
        commit_msg = f"upload file {file.filename}"

        res = requests.put(
            github_api,
            auth=(GITHUB_USERNAME, GITHUB_TOKEN),
            json={
                "message": commit_msg,
                "content": b64_content,
                "branch": "main"
            }
        )

        if res.status_code in [200, 201]:
            urls.append(f"{CDN_URL}{file.filename}")
        else:
            return jsonify({"error": f"Gagal upload {file.filename}", "detail": res.text}), 500

    return jsonify({"urls": urls})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)