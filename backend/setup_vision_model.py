#!/usr/bin/env python3
"""
Setup script to ensure Ollama vision model is available.
Run this before using medicine image analysis feature.
"""

import subprocess
import sys

def check_ollama_installed():
    """Check if Ollama is installed and running."""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Ollama is installed: {result.stdout.strip()}")
            return True
        return False
    except FileNotFoundError:
        print("✗ Ollama is not installed or not in PATH")
        return False

def check_model_available(model_name):
    """Check if a model is already pulled."""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if model_name in result.stdout:
            print(f"✓ Model '{model_name}' is already available")
            return True
        return False
    except Exception as e:
        print(f"Error checking models: {e}")
        return False

def pull_model(model_name):
    """Pull a model from Ollama."""
    print(f"\n📥 Pulling model '{model_name}'...")
    print("This may take a few minutes depending on model size and internet speed.\n")
    
    try:
        subprocess.run(['ollama', 'pull', model_name], check=True)
        print(f"\n✓ Successfully pulled '{model_name}'")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to pull '{model_name}'")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Ollama Vision Model Setup")
    print("=" * 60)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("\n⚠️  Ollama is not installed.")
        print("Please install Ollama from: https://ollama.ai")
        print("Then ensure the Ollama service is running.")
        sys.exit(1)
    
    # Check required models
    models_to_check = [
        ('llava', 'Vision model for medicine image analysis'),
        ('llama3', 'Text model for symptom analysis')
    ]
    
    print("\nChecking required models...\n")
    
    missing_models = []
    for model_name, description in models_to_check:
        print(f"Checking {model_name}... ({description})")
        if not check_model_available(model_name):
            missing_models.append(model_name)
            print(f"  → Not available, will need to pull")
        print()
    
    if not missing_models:
        print("✓ All required models are available!")
        print("\nYou're ready to use the medicine image analysis feature.")
        return
    
    # Pull missing models
    print(f"Found {len(missing_models)} missing model(s). Starting download...\n")
    
    all_success = True
    for model_name in missing_models:
        if not pull_model(model_name):
            all_success = False
    
    print("\n" + "=" * 60)
    if all_success:
        print("✓ Setup complete! All models are ready.")
        print("You can now use the medicine image analysis feature.")
    else:
        print("⚠️  Some models failed to download.")
        print("Please check your internet connection and try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
