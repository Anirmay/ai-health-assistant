import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv

# Load .env file first
load_dotenv()

sys.path.insert(0, '.')

from ai_module.ollama_service import OllamaService

print("Testing Ollama Service...")
print(f"OLLAMA_MODEL from env: {os.getenv('OLLAMA_MODEL')}")
ollama = OllamaService()
print(f"Ollama available: {ollama.is_available}")

if ollama.is_available:
    print("\n" + "="*70)
    print("TEST 1: Simple greeting")
    print("="*70)
    result = ollama.chat_answer("Hi")
    print(f"Response: {result['answer']}")
    print(f"Disclaimer: {result.get('disclaimer', '')}")
    
    print("\n" + "="*70)
    print("TEST 2: Symptom question")
    print("="*70)
    result = ollama.chat_answer("I have a fever of 101 degrees")
    print(f"Response: {result['answer']}")
    print(f"Disclaimer: {result.get('disclaimer', '')}")
    
    print("\n" + "="*70)
    print("TEST 3: Serious symptom")
    print("="*70)
    result = ollama.chat_answer("I have chest pain and breathing difficulty")
    print(f"Response: {result['answer']}")
    print(f"Disclaimer: {result.get('disclaimer', '')}")
else:
    print("Ollama is not available!")
