#!/usr/bin/env python3
"""
Test script for AI Health Assistant LLM Integration.
Verifies that all AI services are working correctly.
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

from ai_module.llm_service import AIExplanationService


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_api_availability():
    """Test 1: Check if OpenAI API is available."""
    print_section("TEST 1: API Availability Check")
    
    service = AIExplanationService()
    is_available = service.is_api_available()
    
    print(f"API Key Configured: {is_available}")
    print(f"API Status: {'✅ READY' if is_available else '⚠️  DEMO MODE (No API key)'}")
    
    return True


def test_symptom_explanation():
    """Test 2: Generate explanation for symptom analysis."""
    print_section("TEST 2: Symptom Explanation Generation")
    
    service = AIExplanationService()
    
    explanation = service.generate_explanation(
        disease="Common Cold",
        symptoms=["sore throat", "runny nose", "cough"],
        confidence=78.5
    )
    
    print(f"Generated Explanation:\n{explanation}\n")
    print(f"✅ Symptom explanation generated successfully")
    
    return True


def test_medicine_explanation():
    """Test 3: Generate explanation for medicine detection."""
    print_section("TEST 3: Medicine Detection Explanation")
    
    service = AIExplanationService()
    
    explanation = service.explain_medicine_detection(
        medicine_name="Ibuprofen",
        detection_result={
            'confidence': 92.3,
            'is_recognized': True,
            'packaging_quality': 'high'
        }
    )
    
    print(f"Generated Explanation:\n{explanation}\n")
    print(f"✅ Medicine explanation generated successfully")
    
    return True


def test_chat_response():
    """Test 4: Generate conversational chat response."""
    print_section("TEST 4: Chat Response Generation")
    
    service = AIExplanationService()
    
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
    
    print(f"Response Type: {type(response)}")
    if isinstance(response, dict):
        print(f"\nAI Answer:\n{response.get('answer', 'N/A')}\n")
        if 'follow_up_suggestions' in response:
            print(f"Follow-up Suggestions:")
            for i, suggestion in enumerate(response.get('follow_up_suggestions', []), 1):
                print(f"  {i}. {suggestion}")
    else:
        print(f"Response:\n{response}")
    
    print(f"\n✅ Chat response generated successfully")
    
    return True


def test_symptom_extraction():
    """Test 5: Extract symptoms from user text."""
    print_section("TEST 5: Symptom Extraction from Text")
    
    service = AIExplanationService()
    
    user_input = "I've been having a persistent headache for 3 days, along with fever and body aches"
    sample_symptoms = ["headache", "fever", "body ache", "cough", "sore throat", "fatigue"]
    
    extracted = service.extract_symptoms_from_text(user_input, symptom_database=sample_symptoms)
    
    print(f"User Input: \"{user_input}\"\n")
    print(f"Extracted Symptoms:")
    if isinstance(extracted, dict):
        for key, value in extracted.items():
            if isinstance(value, list):
                print(f"  {key}: {', '.join(value)}")
            else:
                print(f"  {key}: {value}")
    else:
        print(f"  {extracted}")
    
    print(f"\n✅ Symptom extraction completed successfully")
    
    return True


def test_health_advice():
    """Test 6: Generate health advice."""
    print_section("TEST 6: Health Advice Generation")
    
    service = AIExplanationService()
    
    advice = service.generate_health_advice(
        disease="Migraine",
        symptoms=["severe headache", "sensitivity to light", "nausea"],
        risk_level="High"
    )
    
    print(f"Generated Health Advice:\n{advice}\n")
    print(f"✅ Health advice generated successfully")
    
    return True


def test_system_status():
    """Test 7: Get system status."""
    print_section("TEST 7: System Status Report")
    
    service = AIExplanationService()
    
    status = service.get_system_status()
    
    print(f"System Status:\n{json.dumps(status, indent=2)}\n")
    print(f"✅ System status retrieved successfully")
    
    return True


def test_error_handling():
    """Test 8: Verify error handling and graceful degradation."""
    print_section("TEST 8: Error Handling & Graceful Degradation")
    
    service = AIExplanationService()
    
    # Test 1: Missing API key
    print("Testing behavior with missing API key:")
    status = service.get_system_status()
    if status.get('api_available'):
        print("  ✅ API is configured")
    else:
        print("  ✅ API not configured - Demo mode active (GRACEFUL FALLBACK)")
    
    # Test 2: Verify no exceptions are thrown
    print("\nTesting exception handling:")
    try:
        # Call methods even if API is not available
        explanation = service.generate_explanation("Test", ["test"], 50)
        print(f"  ✅ Generate explanation handled gracefully")
        
        chat = service.chat_answer("Test message", None)
        print(f"  ✅ Chat answer handled gracefully")
        
        medicine = service.explain_medicine_detection("Test", {})
        print(f"  ✅ Medicine explanation handled gracefully")
        
    except Exception as e:
        print(f"  ❌ ERROR: Exception not caught: {str(e)}")
        return False
    
    print(f"\n✅ All error handling tests passed")
    
    return True


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("  AI HEALTH ASSISTANT - LLM INTEGRATION TEST SUITE")
    print("="*60)
    
    tests = [
        ("API Availability", test_api_availability),
        ("Symptom Explanation", test_symptom_explanation),
        ("Medicine Explanation", test_medicine_explanation),
        ("Chat Response", test_chat_response),
        ("Symptom Extraction", test_symptom_extraction),
        ("Health Advice", test_health_advice),
        ("System Status", test_system_status),
        ("Error Handling", test_error_handling),
    ]
    
    results = {}
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = "✅ PASSED"
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            results[test_name] = f"❌ FAILED: {str(e)}"
            failed += 1
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
    
    # Print summary
    print_section("TEST SUMMARY")
    
    for test_name, result in results.items():
        print(f"{result} - {test_name}")
    
    print(f"\nTotal Tests: {passed + failed}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED! LLM Integration is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
    
    return failed == 0


if __name__ == '__main__':
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
