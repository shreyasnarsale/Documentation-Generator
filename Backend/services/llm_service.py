import os
import time
from typing import Dict
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# Load environment variables
load_dotenv()


def generate_documentation(file_structure: Dict) -> Dict:
    """
    Generates professional Markdown documentation
    using Gemini 2.5 Flash (low-cost & stable).
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    files_content = ""
    languages = set()
    start_time = time.time()

    max_files = 2  # Keep small for cost safety

    for file_path in file_structure.get("files", [])[:max_files]:
        ext = os.path.splitext(file_path)[1]
        if ext:
            languages.add(ext[1:])

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()[:1500]  # Strong limit to reduce tokens
                files_content += (
                    f"\n--- File: {os.path.basename(file_path)} ---\n"
                    f"{content}\n"
                )
        except Exception:
            continue

    prompt = f"""
You are a senior software architect.

Generate clean, professional Markdown documentation.

Include:
1. Project Overview
2. Architecture
3. Installation & Setup
4. Key Components & Responsibilities
5. API Reference (if applicable)

Project Structure:
{file_structure.get("tree", "")}

Source Code:
{files_content}
"""

    # Small delay to avoid burst RPM limit
    time.sleep(1)

    tokens_used = 0
    documentation = ""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        documentation = response.text

        # Extract token usage safely
        if hasattr(response, "usage") and response.usage:
            tokens_used = getattr(response.usage, "total_token_count", 0)

    except ClientError as e:
        # Graceful handling of quota errors
        if "RESOURCE_EXHAUSTED" in str(e):
            raise Exception("Rate limit exceeded. Please wait 30–60 seconds and try again.")
        raise e

    return {
        "documentation": documentation,
        "metadata": {
            "totalFiles": len(file_structure.get("files", [])),
            "languages": list(languages),
            "processingTime": round(time.time() - start_time, 2),
            "tokensUsed": tokens_used,
        },
    }
