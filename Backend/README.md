# Backend - FastAPI Application

FastAPI backend with Google Gemini LLM integration.

## Quick Start

1. Install UV (if not already installed):

   ```bash
   pip install uv
   ```

2. Create virtual environment:

   ```bash
   uv venv
   ```

3. Activate virtual environment:

   **On Windows:**
   ```bash
   .venv\Scripts\activate
   ```

   **On macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   uv add -r requirements.txt
   ```

5. Create a `.env` file with your Google API key:

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

6. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

The server will start at http://localhost:8000

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/random-quote` - Generate random quote using Gemini LLM

For detailed setup instructions, see the main [README.md](../README.md) file.
