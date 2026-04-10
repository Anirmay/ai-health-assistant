#!/usr/bin/env pwsh
# Quick startup script for AI Health Assistant Chat API (Windows PowerShell)
# This script starts both Ollama and the Flask API

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      🏥 AI Health Assistant Chat API - Quick Start         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is installed
$ollamaCheck = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaCheck) {
    Write-Host "⚠️  Ollama is not installed or not in PATH" -ForegroundColor Yellow
    Write-Host "   Download from: https://ollama.ai" -ForegroundColor Yellow
    Write-Host "   After installing, close and reopen this PowerShell window" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is available
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCheck) {
    $pythonCheck = Get-Command py -ErrorAction SilentlyContinue
    if (-not $pythonCheck) {
        Write-Host "⚠️  Python is not installed or not in PATH" -ForegroundColor Yellow
        Write-Host "   Please install Python 3.8 or higher from https://python.org" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    $pythonCmd = "py"
} else {
    $pythonCmd = "python"
}

# Step 1: Check Ollama Model
Write-Host "Step 1: Checking Ollama Model" -ForegroundColor Blue
Write-Host "   Ensuring llama3 model is available..."

$modelCheck = &ollama list | Select-String "llama3"
if (-not $modelCheck) {
    Write-Host "   📥 Installing llama3 model (this may take a few minutes)..."
    Write-Host "   Please wait..." -ForegroundColor Yellow
    &ollama pull llama3
} else {
    Write-Host "   ✅ llama3 model is installed" -ForegroundColor Green
}

# Step 2: Check Ollama Service
Write-Host ""
Write-Host "Step 2: Checking Ollama Service" -ForegroundColor Blue

$maxAttempts = 10
$attempt = 0
$ollamaRunning = $false

do {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ollamaRunning = $true
            Write-Host "   ✅ Ollama is already running" -ForegroundColor Green
            break
        }
    } catch {
        # Ollama not responding yet
    }
    
    $attempt++
    if ($attempt -eq 1) {
        Write-Host "   Waiting for Ollama to start (start it manually if not running)..."
        Write-Host "   Run in another PowerShell: ollama serve" -ForegroundColor Yellow
    }
    
    Start-Sleep -Seconds 1
} while ($attempt -lt $maxAttempts)

if (-not $ollamaRunning) {
    Write-Host "   ⚠️  Ollama does not appear to be running" -ForegroundColor Yellow
    Write-Host "   Please start Ollama manually in another PowerShell window:" -ForegroundColor Yellow
    Write-Host "   > ollama serve" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter once Ollama is running to continue"
}

# Step 3: Install Python Dependencies
Write-Host ""
Write-Host "Step 3: Installing Python Dependencies" -ForegroundColor Blue
Write-Host "   Running: pip install -r requirements.txt"
Write-Host ""

& $pythonCmd -m pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Some dependencies may not have installed correctly" -ForegroundColor Yellow
    Write-Host "   Try running manually: pip install -r requirements.txt" -ForegroundColor Yellow
}

Write-Host "   ✅ Dependencies installed" -ForegroundColor Green

# Step 4: Start Flask API
Write-Host ""
Write-Host "Step 4: Starting Flask API" -ForegroundColor Blue
Write-Host "   Running: python chat_app.py"
Write-Host "   API will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "   Endpoints:"
Write-Host "   • POST http://localhost:5000/api/chat - Chat with AI"
Write-Host "   • GET  http://localhost:5000/api/health - Health check"
Write-Host "   • GET  http://localhost:5000/api/status - Service status"
Write-Host "   • GET  http://localhost:5000/api/stats - Statistics"
Write-Host ""
Write-Host "   Press Ctrl+C to stop the API" -ForegroundColor Yellow
Write-Host ""

& $pythonCmd chat_app.py

Read-Host "Press Enter to exit"
