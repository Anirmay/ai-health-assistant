#!/usr/bin/env python3
"""
Quick test script to verify Ollama models are working.
"""

import ollama
import base64
import os
from pathlib import Path

def test_text_model():
    """Test llama3 text model."""
    print("=" * 60)
    print("Testing Text Model (llama3)")
    print("=" * 60)
    
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{
                "role": "user",
                "content": "Briefly explain what aspirin is used for."
            }],
            stream=False
        )
        
        print("✓ Text model is working!")
        print(f"\nResponse: {response['message']['content']}\n")
        return True
        
    except Exception as e:
        print(f"✗ Text model failed: {e}\n")
        return False

def test_vision_model():
    """Test llava vision model with a sample image."""
    print("=" * 60)
    print("Testing Vision Model (llava)")
    print("=" * 60)
    
    # Check if a test image exists
    test_image_paths = [
        "test_medicine.jpg",
        "test_medicine.png",
        "../frontend/src/assets/test.jpg"
    ]
    
    image_path = None
    for path in test_image_paths:
        if os.path.exists(path):
            image_path = path
            break
    
    if not image_path:
        print("⚠️  No test image found.")
        print("To test vision model, provide a test image (test_medicine.jpg or test_medicine.png)")
        print("\nSkipping vision test. Please test manually from the app after setup.\n")
        return None
    
    try:
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        print(f"Testing with image: {image_path}")
        
        response = ollama.chat(
            model="llava",
            messages=[{
                "role": "user",
                "content": "Is this a medicine or pharmaceutical product? Answer YES or NO.",
                "images": [image_base64]
            }],
            stream=False
        )
        
        print("✓ Vision model is working!")
        print(f"\nResponse: {response['message']['content']}\n")
        return True
        
    except Exception as e:
        print(f"✗ Vision model failed: {e}\n")
        return False

def list_available_models():
    """List all available Ollama models."""
    print("=" * 60)
    print("Available Ollama Models")
    print("=" * 60)
    
    try:
        models = ollama.list()
        
        if not models.get('models'):
            print("✗ No models found. Run 'ollama pull llama3' and 'ollama pull llava'\n")
            return False
        
        print("Installed models:\n")
        for model in models['models']:
            name = model.get('name', 'Unknown')
            size = model.get('size', 0)
            size_gb = size / (1024**3)
            print(f"  • {name} ({size_gb:.1f} GB)")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ Failed to list models: {e}\n")
        return False

def main():
    print("\n🧪 Ollama Health Check\n")
    
    # Step 1: Check available models
    models_ok = list_available_models()
    
    # Step 2: Test text model
    text_ok = test_text_model()
    
    # Step 3: Test vision model  
    vision_ok = test_vision_model()
    
    # Summary
    print("=" * 60)
    print("Health Check Summary")
    print("=" * 60)
    
    if text_ok and (vision_ok is True or vision_ok is None):
        print("✓ Core models are functional!")
        print("\nYou're ready to use the AI health assistant.")
        if vision_ok is None:
            print("Vision model (llava) not tested yet. Test it in the app with real medicine images.")
    elif not text_ok:
        print("✗ Text model (llama3) is not working.")
        print("Run: ollama pull llama3")
    elif vision_ok is False:
        print("✗ Vision model (llava) is not working.")
        print("Run: ollama pull llava")
        print("\nText model works, so symptom analyzer should work.")
    
    print()

if __name__ == '__main__':
    main()
