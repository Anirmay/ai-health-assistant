#!/bin/bash
# Quick startup script for AI Health Assistant Chat API
# This script starts both Ollama and the Flask API

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      🏥 AI Health Assistant Chat API - Quick Start         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
END='\033[0m'

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️  Ollama is not installed${END}"
    echo "   Download from: https://ollama.ai"
    echo "   Or install with: brew install ollama (macOS)"
    exit 1
fi

# Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python is not installed${END}"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${BLUE}Step 1: Checking Ollama Model${END}"
echo "   Ensuring llama3 model is available..."

if ollama list | grep -q "llama3"; then
    echo -e "${GREEN}   ✅ llama3 model is installed${END}"
else
    echo "   📥 Installing llama3 model (this may take a few minutes)..."
    ollama pull llama3
fi

echo ""
echo -e "${BLUE}Step 2: Starting Ollama Service${END}"
echo "   Running: ollama serve"
echo "   This will keep running in the background"
echo ""

# Start Ollama in background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "   Waiting for Ollama to start..."
sleep 3

# Check if Ollama is running
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}   ✅ Ollama is ready!${END}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${YELLOW}   ⚠️  Ollama not responding, but continuing...${END}"
    fi
    sleep 1
done

echo ""
echo -e "${BLUE}Step 3: Installing Python Dependencies${END}"
echo "   Running: pip install -r requirements.txt"
pip install -q -r requirements.txt
echo -e "${GREEN}   ✅ Dependencies installed${END}"

echo ""
echo -e "${BLUE}Step 4: Starting Flask API${END}"
echo "   Running: python chat_app.py"
echo "   API will be available at: http://localhost:5000"
echo ""
echo "   Endpoints:"
echo "   • POST http://localhost:5000/api/chat - Chat with AI"
echo "   • GET  http://localhost:5000/api/health - Health check"
echo "   • GET  http://localhost:5000/api/status - Service status"
echo "   • GET  http://localhost:5000/api/stats - Statistics"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both services${END}"
echo ""

# Run Flask app
trap "kill $OLLAMA_PID; exit" INT TERM
python chat_app.py
