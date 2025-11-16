@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask backend on http://localhost:5000
echo Starting frontend server on http://localhost:8000
echo.

start cmd /k "python app.py"
timeout /t 2 /nobreak >nul
start cmd /k "python -m http.server 8000"

echo.
echo Both servers are starting!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
pause

