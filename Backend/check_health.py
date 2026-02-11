import requests
import sys

try:
    response = requests.get("http://localhost:8000/api/health", timeout=5)
    if response.status_code == 200:
        print("Backend is running properly. Health check passed.")
        print(response.json())
        sys.exit(0)
    else:
        print(f"Backend returned status code: {response.status_code}")
        print(response.text)
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print("Backend is NOT reachable. Connection refused.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
