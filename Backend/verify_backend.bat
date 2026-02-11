@echo off
echo Verifying Backend Imports...
cd /d "%~dp0"
"C:\Users\Shreyas\AppData\Local\Programs\Python\Python312\python.exe" diagnose_backend.py
echo.
echo If you see an error above, please copy and report it.
pause
