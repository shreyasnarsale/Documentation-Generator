
# 🚀 Documentation Generator from Code

AI-powered full-stack application that generates complete project documentation from a ZIP file of your codebase and allows you to chat with your documentation using RAG (Retrieval-Augmented Generation).

---

## 📌 Project Overview

Documentation Generator from Code is a full-stack AI application that:

* 📂 Uploads a full project as a ZIP file
* 🤖 Uses Google Gemini LLM to analyze the entire codebase
* 📝 Generates structured Markdown documentation
* 💬 Allows interactive RAG-based chat with the documentation
* 📤 Exports documentation as Markdown

No database is used. Everything works session-based and in-memory.

---

# 🏗 Architecture Overview

Frontend (React + Vite + Tailwind)
⬇
FastAPI Backend
⬇
Google Gemini LLM (Large Context)
⬇
LangChain + FAISS (RAG Vector Store)

---

# 🛠 Tech Stack

## Frontend

* React 19
* Vite
* Tailwind CSS
* React Router DOM
* Firebase Authentication
* react-markdown
* react-syntax-highlighter

## Backend

* Python 3.12+
* FastAPI
* Uvicorn
* LangChain
* Google Gemini API
* FAISS (Vector Store)
* Pydantic

## AI

* Gemini LLM (Large Context)
* Gemini Embeddings
* RAG (Retrieval-Augmented Generation)

---

# 📂 Project Structure

```
Documentation-Generator/
│
├── Backend/
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── Frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── .env
│
└── README.md
```

---

# ⚙️ Installation Guide

---

# 🔧 Backend Setup (FastAPI)

### 1️⃣ Go to backend folder

```
cd Backend
```

### 2️⃣ Create virtual environment

```
python -m venv backend-env
```

### 3️⃣ Activate environment

Windows:

```
backend-env\Scripts\activate
```

Mac/Linux:

```
source backend-env/bin/activate
```

### 4️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## 🔑 Create Backend .env File

Create a file inside Backend folder named:

```
.env
```

Add:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

⚠️ Important:
Never upload `.env` file to GitHub.

---

## ▶️ Start Backend Server

```
uvicorn main:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

API Docs available at:

```
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup (React + Vite)

### 1️⃣ Go to frontend folder

```
cd Frontend
```

### 2️⃣ Install dependencies

```
npm install
```

---

## 🔑 Create Frontend .env File

Create:

```
Frontend/.env
```

Add:

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## ▶️ Start Frontend

```
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🚀 How to Use

1. Open frontend in browser
2. Signup / Login
3. Upload a ZIP file of your project
4. Wait for AI to generate documentation
5. View formatted documentation
6. Use Chat feature to ask questions
7. Export documentation if needed

---

# 📡 API Endpoints

| Method | Endpoint                 | Description                |
| ------ | ------------------------ | -------------------------- |
| GET    | /api/health              | Health check               |
| POST   | /api/upload-and-generate | Upload ZIP & generate docs |
| POST   | /api/export-markdown     | Export docs                |
| POST   | /api/chat/initialize     | Initialize chat            |
| POST   | /api/chat/message        | Send chat message          |

---

# 🔐 Security Features

* ZIP validation before extraction
* Temporary file handling using `tempfile`
* No execution of uploaded code
* In-memory vector store (no persistent storage)
* Firebase authentication

---

# 💬 RAG Chat Flow

1. Documentation converted to embeddings
2. Stored in FAISS vector store
3. User asks question
4. Relevant sections retrieved
5. LLM generates context-aware answer

---

# 🌍 Deployment Guide

## Backend Deployment (Example: Render)

Start Command:

```
uvicorn main:app --host 0.0.0.0 --port 10000
```

Add environment variable:

```
GEMINI_API_KEY=your_key
```

---

## Frontend Deployment (Example: Vercel)

Add environment variable:

```
VITE_API_BASE_URL=https://your-backend-url
```

---

# 📈 Future Improvements

* Add PDF export
* Persistent documentation storage
* Chat history saving
* Code visualization
* Multi-user collaboration
* Dark/light toggle
* Usage analytics dashboard

---

# 🎯 Why This Project is Strong

* Full-stack development
* AI integration
* RAG implementation
* Large context LLM usage
* Modern UI design
* No database architecture
* Production-ready structure

---

🚀 **Live Demo:**  
👉 https://documentation-generator-project.netlify.app/

---

## 📌 Project Overview
This project automatically generates documentation from code...

---

# 👨‍💻 Author

**Shreyas Narsale**
BE Information Technology
AI & Full Stack Developer

GitHub: [https://github.com/shreyasnarsale](https://github.com/shreyasnarsale)

---

# ⭐ Final Note

This project demonstrates practical AI integration with real-world full-stack architecture and shows strong understanding of:

* API design
* LLM integration
* RAG systems
* File processing
* Authentication
* Deployment
