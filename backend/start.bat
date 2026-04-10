@echo off
REM Quick startup script for AI Health Assistant Chat API (Windows)
REM This script starts both Ollama and the Flask API

setlocal enabledelayedexpansion

echo.
echo.╔════════════════════════════════════════════════════════════╗
echo.║      🏥 AI Health Assistant Chat API - Quick Start         ║
echo.╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama is not installed or not in PATH
    echo    Download from: https://ollama.ai
    echo    After installing, close and reopen this command prompt
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Python is not installed or not in PATH
        echo    Please install Python 3.8 or higher from https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo Step 1: Checking Ollama Model
echo    Ensuring llama3 model is available...

ollama list | find "llama3" >nul
if errorlevel 1 (
    echo    📥 Installing llama3 model (this may take a few minutes)...
    echo    Please wait...
    ollama pull llama3
) else (
    echo    ✅ llama3 model is installed
)

echo.
echo Step 2: Starting Ollama Service
echo    You need to start Ollama in a separate terminal:
echo.
echo    1. Open a NEW command prompt or PowerShell
echo    2. Run: ollama serve
echo    3. Leave it running and return to this window
echo    4. Press any key to continue...
echo.

pause

echo.
echo Step 3: Installing Python Dependencies
echo    Running: pip install -r requirements.txt
echo.

%PYTHON_CMD% -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo ⚠️  Some dependencies may not have installed correctly
    echo    Try running manually: pip install -r requirements.txt
)

echo    ✅ Dependencies installed
echo.

echo Step 4: Starting Flask API
echo    Running: python chat_app.py
echo    API will be available at: http://localhost:5000
echo.
echo    Endpoints:
echo    • POST http://localhost:5000/api/chat - Chat with AI
echo    • GET  http://localhost:5000/api/health - Health check
echo    • GET  http://localhost:5000/api/status - Service status
echo    • GET  http://localhost:5000/api/stats - Statistics
echo.
echo    Press Ctrl+C to stop the API
echo.

%PYTHON_CMD% chat_app.py

pause
