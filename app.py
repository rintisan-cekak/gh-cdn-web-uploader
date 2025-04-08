import os
import base64
import requests
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_API_URL = os.getenv("REPO_URL")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
CDN_URL = os.getenv("CDN_URL")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if not file.mimetype.startswith("image/"):
        return jsonify({"error": "Only image files are allowed"}), 400
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_content = base64.b64encode(file.read()).decode("utf-8")
    filename = file.filename

    github_api_url = f"{REPO_API_URL}/contents/{UPLOAD_FOLDER}/{filename}"

    payload = {
        "message": f"upload file {filename}",
        "content": file_content,
        "branch": "main"  # Ubah jika repo default branch-nya bukan main
    }

    # check if file exists to include sha for replacement
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    existing_file = requests.get(github_api_url, headers=headers)
    if existing_file.status_code == 200:
        payload["sha"] = existing_file.json()["sha"]

    response = requests.put(github_api_url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        return jsonify({
            "message": "File uploaded successfully",
            "url": f"{CDN_URL}{filename}"
        }), 200
    else:
        return jsonify({"error": "Failed to upload", "details": response.json()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
