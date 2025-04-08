
# 📤 GitHub Image Uploader
## gh-cdn-web-uploader
A lightweight, browser-based tool that allows users to upload image files directly to a public GitHub repository using drag & drop or file picker interface. Built with Flask (Python) on the backend and pure HTML5/JavaScript on the frontend. Fully Dockerized for easy deployment.

---

## ✨ Features

- ✅ Drag & drop or select image files from your device
- 🖼️ Instant preview before upload
- 🚫 File protection: Only image files are allowed (`image/*`)
- 🧠 Upload delay mechanism with `Lanjut` and `Cancel` options
- 🔁 Overwrites existing files if they share the same name (GitHub handles versioning)
- 💬 Commit message: `upload file <filename>`
- 🌐 After upload, get the direct CDN link using configured `CDN_URL`
- ⚡ Animated success feedback & reset feature for user experience
- 📦 Dockerized for easy deployment and portability

---

## 🔧 Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **GitHub API**: Authenticated via personal access token (PAT)
- **Deployment**: Docker & Docker Compose

---

## 🗂️ Project Structure

```bash
.
├── app.py               # Flask backend
├── templates/
│   └── index.html       # HTML frontend interface
├── .env                 # GitHub credentials & settings
├── Dockerfile           # Docker build instructions
├── docker-compose.yml   # Docker service definition
└── README.md
```

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the following content:

```env
GITHUB_USERNAME=your-username
GITHUB_TOKEN=your-personal-access-token
REPO_URL=https://api.github.com/repos/your-username/your-repo
UPLOAD_FOLDER=images
CDN_URL=https://your-github.io-url/images/
```

> 💡 You must use a **Personal Access Token** with `repo` scope if uploading to private repositories. Public repos only require basic access.

---

## 🚀 Running the App (Dockerized)

### 1. Build and Run

```bash
docker-compose up --build
```

This will start the app at [http://localhost:5000](http://localhost:5000)

### 2. Access via Browser

Open your browser and go to:

```
http://localhost:5000
```

---

## 🧪 How to Use

1. Drag and drop or select an image file.
2. Preview appears in center of screen.
3. Choose:
   - `❌ Cancel` to discard the file
   - `✅ Lanjut` to upload to GitHub
4. On success:
   - Success message with direct CDN URL appears
   - Includes note: *"URL Resolve butuh beberapa saat untuk aktif, jika akses URL belum aktif coba lagi beberapa saat."*
5. Optionally click `🔄 Reset` to start a new upload.

---


## 🚧 Limitations

- Only supports image files (`image/*`)
- GitHub will replace files with the same name without versioning
- CDN propagation delay (jsDelivr) may require a few seconds post-upload

---

## 📜 License

MIT License

---

## 🙏 Credits

Made with ❤️ using Flask & GitHub API  
Maintained by @rintisancekak