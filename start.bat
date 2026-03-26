@echo off
title IMS Project

:: Change to the directory where this .bat file is located
cd /d "%~dp0"

echo Starting Flask backend...
start "Flask Backend" cmd /k "python backend/app.py"

:: Wait a couple seconds for Flask to initialize
timeout /t 3 /nobreak > nul

echo Opening index.html in browser...
start "" "frontend\index.html"

echo.
echo IMS Project is running!
echo Close the Flask Backend window to stop the server.
