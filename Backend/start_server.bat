@echo off
echo Starting Backend Server...
cd /d "%~dp0"
"C:\Users\Shreyas\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
"C:\Users\Shreyas\AppData\Local\Programs\Python\Python312\python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
