
"""
Backend - FastAPI Application
Documentation Generator from Code

Available Endpoints:
    GET /                    - Welcome message
    GET /api/health          - Health check endpoint
    POST /api/upload-and-generate - Upload ZIP and generate documentation
    POST /api/export-markdown - Export documentation as Markdown file
    POST /api/chat/initialize - Initialize RAG vector store for chat
    POST /api/chat/message   - Send chat message and get response

To run this server:
    uvicorn main:app --reload

The server will start at: http://localhost:8000
API documentation will be available at: http://localhost:8000/docs
"""

import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Documentation Generator API",
    description="Backend API for Documentation Generator from Code project",
    version="0.1.0"
)

# Enable CORS (Cross-Origin Resource Sharing) to allow frontend to connect
# This is necessary because the frontend runs on a different port than the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port and common React port
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Check for required environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("Warning: GEMINI_API_KEY not found in environment variables.")
    print("Please create a .env file with: GEMINI_API_KEY=your_api_key_here")
    print("Get your API key from: https://makersuite.google.com/app/apikey")

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Documentation Generator API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

from api import upload, export, chat
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(export.router, prefix="/api", tags=["export"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])