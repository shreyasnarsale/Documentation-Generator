import requests
import sys

try:
    response = requests.get("http://127.0.0.1:8000/api/health", timeout=5)
    with open("health_status_result.txt", "w") as f:
        f.write(f"Status: {response.status_code}\n")
        f.write(f"Body: {response.text}\n")
except Exception as e:
    with open("health_status_result.txt", "w") as f:
        f.write(f"Error: {e}\n")
