# Documentation Generator from Code - Project Documentation

This document provides comprehensive documentation for the Documentation Generator from Code project, including architecture overview, API endpoints, issue flow, and development guidelines.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [API Endpoints](#api-endpoints)
5. [Frontend Structure](#frontend-structure)
6. [Issue Flow](#issue-flow)
7. [Development Guidelines](#development-guidelines)

---

## Project Overview

The Documentation Generator from Code is a full-stack application that allows developers to upload a ZIP file of their entire codebase and automatically generate comprehensive documentation using AI. The application uses Google Gemini LLM with large context windows to analyze complete codebases at once, understanding relationships between files and generating well-formatted Markdown documentation. Additionally, users can chat with their documentation using RAG (Retrieval-Augmented Generation) to ask questions and get instant answers about their codebase.

### Key Features

- User authentication with Firebase
- ZIP file upload of entire codebase
- Automatic extraction and validation of code files
- AI-powered documentation generation with full codebase context
- Comprehensive documentation including project overview, architecture, API reference, and usage examples
- Interactive documentation viewer with syntax highlighting and table of contents
- Export documentation as Markdown file
- RAG chat interface for asking questions about the codebase
- Session-based workflow (no database storage)

### Target Users

- Developers who want to quickly generate documentation for their codebases
- Teams needing to document APIs and full projects
- Open-source contributors creating project documentation
- Students learning code documentation best practices
- Anyone working with undocumented legacy code
- Developers wanting to understand unfamiliar codebases through chat

---

## Architecture

### High-Level Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   React     │────────▶│   FastAPI   │────────▶│  Temp Files │
│  Frontend   │         │   Backend   │         │  (Session)  │
└─────────────┘         └─────────────┘         └─────────────┘
      │                        │
      │                        │
      ▼                        ▼
┌─────────────┐         ┌─────────────┐
│  Firebase   │         │   Gemini    │
│    Auth     │         │     LLM     │
└─────────────┘         └─────────────┘
                              │
                              │
                              ▼
                        ┌─────────────┐
                        │   LangChain  │
                        │  + RAG +    │
                        │  Vector DB  │
                        └─────────────┘
```

### Data Flow

1. **User Authentication**: Firebase handles all authentication on the frontend
2. **ZIP Upload**: User uploads ZIP → Backend receives file → Extracts to temporary directory → Filters code files
3. **Documentation Generation**: Backend sends entire codebase to Gemini LLM via LangChain → LLM analyzes codebase → Generates comprehensive Markdown documentation
4. **Documentation Display**: Generated documentation → Returned to frontend → Displayed in formatted viewer
5. **RAG Chat**: Documentation → Converted to embeddings → Stored in vector store → User asks questions → RAG retrieves relevant context → LLM generates answers
6. **Export**: User clicks export → Backend formats documentation → Returns as downloadable Markdown file

---

## Technology Stack

### Frontend
- **React 19** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router DOM** - Client-side routing
- **Firebase SDK** - Authentication
- **react-markdown** - Markdown rendering
- **react-syntax-highlighter** - Code syntax highlighting

### Backend
- **Python 3.12+** - Programming language
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Python zipfile** - Built-in ZIP extraction (no installation needed)
- **Python tempfile** - Temporary file management

### Database
- **None** - No database required (session-based state management)

### AI/ML
- **LangChain** - LLM integration and RAG framework
- **Google Gemini 2.0 Flash Experimental** - LLM with 1M token context window (FREE tier)
- **FAISS or Chroma** - In-memory vector store for RAG
- **Google Gemini Embeddings** - For RAG vector embeddings

### Authentication
- **Firebase Authentication** - Email/password authentication (frontend only)

---

## API Endpoints

### Endpoint Summary

| Method | Endpoint | Protected | Purpose | LLM Integration | Request Body | Response |
|--------|----------|-----------|---------|----------------|--------------|----------|
| POST | /api/upload-and-generate | Yes | Upload ZIP and generate documentation | Yes | FormData (zipFile, userId) | {sessionId, documentation, fileStructure, metadata} |
| POST | /api/export-markdown | Yes | Export documentation as Markdown file | No | {documentation, filename} | File download (application/octet-stream) |
| POST | /api/chat/initialize | Yes | Initialize RAG vector store for chat | Yes | {sessionId, documentation} | {chatSessionId, status} |
| POST | /api/chat/message | Yes | Send chat message and get response | Yes | {chatSessionId, message, conversationHistory} | {response, sources} |
| GET | /api/health | No | Health check endpoint | No | - | {status, timestamp} |

### Detailed Endpoint Specifications

#### POST /api/upload-and-generate

**Purpose:** Main endpoint that handles ZIP upload, extraction, analysis, and documentation generation.

**Request:**
- FormData with `zipFile` (binary ZIP file) and `userId` (string from Firebase)

**Response:**
```json
{
  "sessionId": "unique-session-id",
  "documentation": "# Complete Markdown Documentation...",
  "fileStructure": {
    "root": "project-name",
    "files": ["file1.py", "file2.js"],
    "tree": "..."
  },
  "metadata": {
    "totalFiles": 25,
    "languages": ["Python", "JavaScript"],
    "processingTime": 15.3,
    "tokensUsed": 45000
  }
}
```

**Processing Steps:**
1. Validate ZIP file (size, type)
2. Extract to temporary directory
3. Filter relevant files (exclude node_modules, .git, etc.)
4. Build file structure tree
5. Read all code files
6. Construct comprehensive prompt for LLM
7. Send to Gemini with full codebase context
8. Parse LLM response
9. Format as structured Markdown
10. Clean up temporary files
11. Return documentation

#### POST /api/chat/initialize

**Purpose:** Initialize RAG vector store for chat functionality.

**Request:**
```json
{
  "sessionId": "session-id-from-upload",
  "documentation": "# Full markdown documentation..."
}
```

**Response:**
```json
{
  "chatSessionId": "chat-session-id",
  "status": "ready",
  "vectorCount": 150
}
```

#### POST /api/chat/message

**Purpose:** Handle chat messages and return RAG-based responses.

**Request:**
```json
{
  "chatSessionId": "chat-session-id",
  "message": "How does the authentication work?",
  "conversationHistory": [
    {"role": "user", "content": "previous question"},
    {"role": "assistant", "content": "previous answer"}
  ]
}
```

**Response:**
```json
{
  "response": "Based on the codebase, authentication works by...",
  "sources": [
    "auth.py: lines 15-30",
    "login.js: lines 45-60"
  ],
  "conversationHistory": [...]
}
```

---

## Frontend Structure

### Pages

| Page Name | Route | Protected | Purpose | Main Components |
|-----------|-------|-----------|---------|----------------|
| Landing | / | No | Welcome page with app info | Navbar, Hero, Features, Footer |
| Signup | /signup | No | User registration | SignupForm |
| Login | /login | No | User authentication | LoginForm |
| Dashboard | /dashboard | Yes | Main dashboard after login | Navbar, Dashboard content |
| Upload | /upload | Yes | Upload ZIP and generate docs | Navbar, ZipUploader, ProcessingStatus |
| Documentation View | /documentation | Yes | View generated documentation | Navbar, DocumentationViewer, ExportButton, ChatButton |
| Chat | /chat | Yes | Chat with documentation | Navbar, ChatInterface, DocumentationSidebar |

### Key Components

| Component Name | Used On Pages | Purpose |
|----------------|---------------|---------|
| Navbar | All pages | Navigation header with auth status |
| Hero | Landing | Hero section with CTA |
| Features | Landing | Feature showcase |
| Footer | All pages | Footer with links |
| SignupForm | Signup | Registration form |
| LoginForm | Login | Login form |
| ZipUploader | Upload | Drag-and-drop ZIP upload |
| ProcessingStatus | Upload | Show upload and processing progress |
| DocumentationViewer | Documentation View | Display generated Markdown docs |
| TableOfContents | Documentation View | TOC for navigation |
| ExportButton | Documentation View | Export as Markdown file |
| ChatButton | Documentation View | Open chat interface |
| ChatInterface | Chat | Main chat component |
| ChatMessageList | Chat | Display chat history |
| ChatInputBox | Chat | Input for chat messages |

---

## Issue Flow

### Foundation Phase (Issues 1-8)

**Issue #01: Project Setup**
- Set up project structure, dependencies, and development environment
- README format with UV package manager setup

**Issue #02: Landing Page UI**
- Create static landing page with hero, features, and footer sections

**Issue #03: Signup Page UI**
- Build signup form UI (static, no Firebase integration yet)

**Issue #04: Login Page UI**
- Build login form UI (static, no Firebase integration yet)

**Issue #05: Firebase Auth Setup**
- Configure Firebase project and SDK in frontend

**Issue #06: Integrate Signup with Firebase**
- Connect signup form to Firebase Authentication

**Issue #07: Integrate Login with Firebase**
- Connect login form to Firebase Authentication

**Issue #08: Dashboard UI**
- Create protected dashboard page with navigation

### Core Features Phase (Issues 9-13)

**Issue #09: Upload Page & ZIP Upload**
- Create upload page UI with drag-and-drop
- Backend endpoint for ZIP file upload and extraction

**Issue #10: Documentation Generation with LLM**
- Backend LLM integration for codebase analysis
- Generate comprehensive Markdown documentation

**Issue #11: Documentation Viewer**
- Display generated documentation with syntax highlighting
- Table of contents navigation

**Issue #12: Export Markdown**
- Export documentation as downloadable Markdown file

**Issue #13: RAG Chat with Documentation**
- Initialize vector store from documentation
- Implement RAG chat interface for asking questions

### Testing Phase (Issue 14)

**Issue #14: Final Testing**
- Complete application flow verification
- End-to-end testing and documentation

---

## Development Guidelines

### Key Principles

1. **No Database Storage**: This project uses session-based state management. No SQLite or other databases are used for storing documentation or chat history.

2. **Temporary File Management**: Use Python's built-in `tempfile` module for temporary file storage. Always clean up temporary files after processing.

3. **Large Context LLM**: Leverage Gemini 2.0 Flash Experimental's 1M token context window to send entire codebases at once. No need for chunking or complex preprocessing.

4. **No Specialized Parsers**: Use LLM to understand code as text. No AST parsers or specialized code analysis libraries needed.

5. **Session-Based RAG**: Vector store is created in-memory per session. No persistence between sessions.

### Technology Constraints

**Allowed:**
- React, FastAPI, Firebase Auth, LangChain, Gemini LLM, Python zipfile/tempfile
- FAISS or Chroma for vector stores
- react-markdown, react-syntax-highlighter

**Not Allowed:**
- Databases (SQLite, PostgreSQL, etc.)
- OCR libraries
- AST parsers
- Specialized code analysis tools
- Docker or containerization
- JWT or backend authentication

### Code Analysis Approach

- **NO specialized code parsing libraries** (AST parsers, language-specific parsers)
- **USE LangChain + Gemini LLM** to read and understand code as text
- **Leverage large context window:** Send entire codebase at once (up to 1M tokens)
- LLM will naturally understand:
  - Function signatures, class definitions
  - Relationships between files (imports, calls)
  - Overall architecture and design patterns
  - Data flow and dependencies

### RAG Implementation

- Use LangChain for embeddings and vector store creation
- Chunk documentation appropriately for better retrieval
- Use FAISS or Chroma for in-memory vector store
- Include conversation history for context-aware responses
- Return source citations with answers

### File Upload Security

- Validate ZIP file size (max 100MB recommended)
- Check file extensions before extraction
- Scan for malicious files (executables, scripts)
- Extract to isolated temporary directory
- Never execute uploaded code
- Sanitize file paths to prevent directory traversal

### Free Tier Management (Gemini)

**Recommended Model: Gemini 2.0 Flash Experimental**
- Completely FREE (no credit card required)
- 1M token context window
- 10 requests per minute (RPM)
- 1,500 requests per day (RPD)
- 4 million tokens per minute (TPM)

**Token Optimization:**
- Monitor token usage per request
- Filter unnecessary files (tests, node_modules, build artifacts)
- Most codebases will fit comfortably within 1M token limit

---

## Project Flow Summary

### Complete User Journey

1. **Landing Page**: User sees app features and benefits
2. **Signup**: User creates account with Firebase
3. **Login**: User authenticates and accesses dashboard
4. **Upload**: User uploads ZIP file of codebase
5. **Processing**: Backend extracts files and generates documentation with LLM
6. **View Documentation**: User views formatted documentation with syntax highlighting
7. **Export**: User downloads documentation as Markdown file
8. **Chat**: User asks questions about codebase using RAG chat

### Data Flow

**Upload and Generation:**
```
ZIP File → Frontend Upload → POST /api/upload-and-generate → Backend Receives
→ Extract to Temp Dir (using zipfile module) → Read All Files → Filter/Validate
→ Build File Structure → Construct LLM Prompt with Full Codebase
→ Send to Gemini 2.0 Flash (1M token context) → LLM Analyzes & Generates Docs
→ Format as Markdown → Return to Frontend → Store in React State
→ Cleanup Temp Files (automatic) → Display Documentation
```

**RAG Chat:**
```
Initialize:
User Clicks Chat → POST /api/chat/initialize → Create Embeddings from Documentation
→ Build FAISS Vector Store → Return Chat Session ID → Ready for Questions

Chat:
User Asks Question → POST /api/chat/message → Vector Search on Documentation
→ Retrieve Relevant Sections → Construct Prompt: Question + Context
→ Send to Gemini → Generate Answer → Return with Sources → Display in Chat
```

---

## Success Criteria

### Technical Success
- ZIP file upload works with drag-and-drop
- ZIP extraction and file filtering work correctly
- Firebase authentication functions properly
- LLM integration successfully analyzes complete codebases
- Documentation generation produces comprehensive, accurate content
- Generated documentation includes all sections (overview, API, examples)
- Markdown rendering displays documentation beautifully
- Export functionality downloads proper Markdown files
- RAG vector store initializes correctly from documentation
- Chat interface provides accurate answers with source citations
- Session management works properly (no data leaks between sessions)
- Temporary file cleanup happens automatically

### Learning Success
- Students understand full-stack development workflow
- Students can connect React frontend to FastAPI backend
- Students learn Firebase authentication integration
- Students understand large context LLM capabilities (Gemini 2.0)
- Students learn how to structure effective LLM prompts
- Students understand RAG (Retrieval-Augmented Generation) concepts
- Students learn vector embeddings and similarity search
- Students can handle file uploads and temporary file management
- Students understand Markdown rendering in React
- Students learn session-based state management

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Firebase Authentication](https://firebase.google.com/docs/auth)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Python zipfile Module](https://docs.python.org/3/library/zipfile.html)
- [Python tempfile Module](https://docs.python.org/3/library/tempfile.html)
- [react-markdown](https://github.com/remarkjs/react-markdown)
- [react-syntax-highlighter](https://github.com/react-syntax-highlighter/react-syntax-highlighter)

---

## License

This is a template project for educational purposes.
