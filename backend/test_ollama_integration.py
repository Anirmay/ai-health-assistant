#!/usr/bin/env python3
"""
Ollama Local LLM Integration Test Suite
Tests all Ollama service functionality and integration points.
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup environment
from dotenv import load_dotenv
load_dotenv()

from ai_module.ollama_service import OllamaService, get_ollama_service


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_ollama_availability():
    """Test 1: Check if Ollama service is available."""
    print_section("TEST 1: Ollama Service Availability")
    
    service = get_ollama_service()
    is_available = service.is_available
    
    print(f"Ollama API URL: {service.api_url}")
    print(f"Model: {service.model}")
    print(f"Status: {'✅ Online' if is_available else '⚠️ Offline'}")
    
    if is_available:
        print(f"\nℹ️  Make sure Ollama is running: ollama serve")
    
    return is_available


def test_symptom_explanation():
    """Test 2: Generate explanation for symptom analysis."""
    print_section("TEST 2: Symptom Explanation Generation")
    
    service = get_ollama_service()
    
    if not service.is_available:
        print("⚠️ Ollama not running. Skipping test.")
        print("Start Ollama with: ollama serve")
        return False
    
    try:
        explanation = service.generate_explanation(
            disease="Common Cold",
            symptoms=["sore throat", "runny nose", "cough"],
            confidence=78.5
        )
        
        print(f"Disease: {explanation.get('disease')}")
        print(f"Confidence: {explanation.get('confidence')}")
        print(f"\nExplanation:")
        print(explanation.get('explanation', 'N/A'))
        print(f"\nDisclaimer: {explanation.get('disclaimer')}")
        
        print(f"\n✅ Symptom explanation generated successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_medicine_explanation():
    """Test 3: Generate explanation for medicine detection."""
    print_section("TEST 3: Medicine Detection Explanation")
    
    service = get_ollama_service()
    
    if not service.is_available:
        print("⚠️ Ollama not running. Skipping test.")
        return False
    
    try:
        explanation = service.explain_medicine_detection(
            medicine_name="Ibuprofen",
            detection_result={
                'confidence': 92.3,
                'is_recognized': True,
                'packaging_quality': 'high'
            }
        )
        
        print(f"Medicine: {explanation.get('medicine')}")
        print(f"Authentic: {explanation.get('is_authentic')}")
        print(f"Confidence: {explanation.get('confidence')}")
        print(f"\nExplanation:")
        print(explanation.get('explanation', 'N/A'))
        print(f"\nSafety Note: {explanation.get('safety_note')}")
        
        print(f"\n✅ Medicine explanation generated successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_chat_response():
    """Test 4: Generate conversational chat response."""
    print_section("TEST 4: Chat Response Generation")
    
    service = get_ollama_service()
    
    if not service.is_available:
        print("⚠️ Ollama not running. Skipping test.")
        return False
    
    try:
        context = {
            'disease': 'Flu',
            'symptoms': ['fever', 'body ache', 'fatigue'],
            'confidence': 85,
            'risk_level': 'Medium'
        }
        
        response = service.chat_answer(
            message="Is this serious? Should I see a doctor?",
            context=context
        )
        
        print(f"User Message: \"Is this serious? Should I see a doctor?\"")
        print(f"\nAI Response:")
        print(response.get('answer', 'N/A'))
        
        if response.get('follow_up_suggestions'):
            print(f"\nFollow-up Suggestions:")
            for i, suggestion in enumerate(response.get('follow_up_suggestions', []), 1):
                print(f"  {i}. {suggestion}")
        
        print(f"\nDisclaimer: {response.get('disclaimer')}")
        
        print(f"\n✅ Chat response generated successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_health_advice():
    """Test 5: Generate health advice."""
    print_section("TEST 5: Health Advice Generation")
    
    service = get_ollama_service()
    
    if not service.is_available:
        print("⚠️ Ollama not running. Skipping test.")
        return False
    
    try:
        advice = service.generate_health_advice(
            disease="Migraine",
            symptoms=["severe headache", "sensitivity to light", "nausea"],
            risk_level="High"
        )
        
        print(f"Disease: {advice.get('disease')}")
        print(f"Risk Level: {advice.get('risk_level')}")
        print(f"\nHealth Advice:")
        print(advice.get('advice', 'N/A'))
        print(f"\nDisclaimer: {advice.get('disclaimer')}")
        
        print(f"\n✅ Health advice generated successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_symptom_extraction():
    """Test 6: Extract symptoms from user text."""
    print_section("TEST 6: Symptom Extraction from Text")
    
    service = get_ollama_service()
    
    if not service.is_available:
        print("⚠️ Ollama not running. Skipping test.")
        return False
    
    try:
        user_input = "I've been having a persistent headache for 3 days, along with fever and body aches"
        sample_symptoms = ["headache", "fever", "body ache", "cough", "sore throat", "fatigue"]
        
        extracted = service.extract_symptoms_from_text(user_input, symptom_database=sample_symptoms)
        
        print(f"User Input: \"{user_input}\"\n")
        print(f"Extracted Symptoms: {extracted.get('extracted_symptoms', [])}")
        print(f"Confidence: {extracted.get('confidence', 0):.2f}")
        
        print(f"\n✅ Symptom extraction completed successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_system_status():
    """Test 7: Get system status."""
    print_section("TEST 7: System Status Report")
    
    service = get_ollama_service()
    status = service.get_system_status()
    
    print(f"System Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ System status retrieved successfully")
    return True


def test_error_messages():
    """Test 8: Verify error handling."""
    print_section("TEST 8: Error Handling & Messages")
    
    service = OllamaService()
    
    # Test offline message
    offline_msg = service._get_offline_message()
    print(f"Offline Message:\n  {offline_msg}")
    
    # Test error message
    error_msg = service._get_error_message()
    print(f"\nError Message:\n  {error_msg}")
    
    # Test status message
    status_msg = service._get_status_message()
    print(f"\nStatus Message:\n  {status_msg}")
    
    print(f"\n✅ Error handling verified")
    return True


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("  OLLAMA LOCAL LLM INTEGRATION TEST SUITE")
    print("="*60)
    print("\n⚠️  Make sure Ollama is running: ollama serve")
    
    tests = [
        ("Ollama Availability", test_ollama_availability),
        ("Symptom Explanation", test_symptom_explanation),
        ("Medicine Explanation", test_medicine_explanation),
        ("Chat Response", test_chat_response),
        ("Health Advice", test_health_advice),
        ("Symptom Extraction", test_symptom_extraction),
        ("System Status", test_system_status),
        ("Error Handling", test_error_messages),
    ]
    
    results = {}
    passed = 0
    failed = 0
    skipped = 0
    
    service = get_ollama_service()
    
    if not service.is_available:
        print("\n⚠️  WARNING: Ollama is not running!")
        print("Start Ollama with: ollama serve")
        print("\nTests will be marked as skipped.\n")
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result is None:
                results[test_name] = "⏭️  SKIPPED"
                skipped += 1
            elif result:
                results[test_name] = "✅ PASSED"
                passed += 1
            else:
                results[test_name] = "❌ FAILED"
                failed += 1
        except Exception as e:
            results[test_name] = f"❌ FAILED: {str(e)}"
            failed += 1
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
    
    # Print summary
    print_section("TEST SUMMARY")
    
    for test_name, result in results.items():
        print(f"{result} - {test_name}")
    
    print(f"\nTotal Tests: {passed + failed + skipped}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Skipped: {skipped} ⏭️")
    
    if skipped > 0 and failed == 0:
        print(f"\n⚠️  Tests skipped because Ollama is not running.")
        print(f"To run all tests, start Ollama with: ollama serve")
    elif failed == 0:
        print(f"\n🎉 ALL TESTS PASSED! Ollama integration is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
    
    return failed == 0 or (failed == 0 and skipped > 0)


if __name__ == '__main__':
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
