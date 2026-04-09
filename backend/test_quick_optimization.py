#!/usr/bin/env python3
"""
Quick Optimization Validation Tests
Validates: Speed, Accuracy, Context, Safety
"""

import sys
import time
from ai_module.ollama_service import OllamaService

def test_section(title):
    """Print test section header."""
    print(f"\n{'='*70}")
    print(f"[TEST] {title}")
    print('='*70)

def test_pass(name, details=""):
    """Print passing test."""
    print(f"  [OK] {name} {details}")

def test_fail(name, details=""):
    """Print failing test."""
    print(f"  [FAIL] {name} {details}")

# Initialize service
service = OllamaService()
pass_count = 0
fail_count = 0

print("\n" + "="*70)
print("[*] OPTIMIZATION TEST SUITE - AI HEALTH ASSISTANT")
print("="*70)

# TEST 1: PREDEFINED RESPONSES
test_section("PREDEFINED RESPONSES (Fast, No LLM)")

questions = [
    "How long does fever recovery take?",
    "Should I see a doctor?",
    "What can I do for my symptoms?",
]

for q in questions:
    start = time.time()
    result = service.chat_answer(q)
    elapsed = time.time() - start
    
    if elapsed < 1.0:  # Should be fast
        test_pass(f"'{q[:40]}...' - {elapsed*1000:.0f}ms")
        pass_count += 1
    else:
        test_fail(f"'{q}' - Too slow: {elapsed:.2f}s", "")
        fail_count += 1

# TEST 2: TEMPERATURE EXTRACTION
test_section("TEMPERATURE PARSING & SPECIFICITY")

temps = [
    ("I have 104F", 104.0),
    ("temperature is 39.2C", 102.56),
    ("99.5 degrees fever", 99.5),
]

for text, expected in temps:
    result = service._extract_temperature(text)
    if result and abs(result - expected) < 1:
        test_pass(f"Parse '{text}' -> {result}°F")
        pass_count += 1
    else:
        test_fail(f"Parse '{text}' expected {expected}, got {result}")
        fail_count += 1

# TEST 3: DURATION EXTRACTION
test_section("DURATION EXTRACTION & CONTEXT")

durations = [
    ("fever for a week", "week"),
    ("lasted month", "month"),
    ("got sick today", "today"),
]

for text, expected in durations:
    result = service._extract_duration(text)
    if result and expected.lower() in result.lower():
        test_pass(f"Extract '{text}' -> '{result}'")
        pass_count += 1
    else:
        test_fail(f"Extract '{text}', got '{result}'")
        fail_count += 1

# TEST 4: RESPONSE VALIDATION
test_section("INVALID RESPONSE DETECTION")

invalid = [
    "You have diabetes (diagnosis)",
    "Take ibuprofen 400mg (medicine)",
    "Definitely bacterial (overconfident)",
    "100% viral infection (certainty)",
]

for resp in invalid:
    is_invalid = service._is_invalid_response(resp)
    if is_invalid:
        test_pass(f"Caught: '{resp[:40]}'...")
        pass_count += 1
    else:
        test_fail(f"Missed: '{resp}'")
        fail_count += 1

# TEST 5: TEMPERATURE-SPECIFIC RESPONSES
test_section("CONTEXT-AWARE RESPONSES")

responses = {
    "I have 104F fever": "high/urgent",
    "I have 99F": "mild",
    "fever for a week": "week/doctor",
    "symptoms worsening": "urgent",
}

for query, keywords in responses.items():
    result = service.chat_answer(query)
    answer = result["answer"].lower()
    
    found = any(kw in answer for kw in keywords.split('/'))
    if found:
        test_pass(f"'{query}' -> includes '{keywords}'")
        pass_count += 1
    else:
        test_fail(f"'{query}' missing context", f"expected: {keywords}")
        fail_count += 1

# TEST 6: EMERGENCY ROUTING
test_section("EMERGENCY DETECTION")

emergencies = [
    "Can't breathe",
    "Chest pain severe",
    "I'm unconscious",
]

for emerg in emergencies:
    result = service.chat_answer(emerg)
    answer = result["answer"].lower()
    
    if "immediately" in answer or "emergency" in answer:
        test_pass(f"'{emerg}' -> Emergency response")
        pass_count += 1
    else:
        test_fail(f"'{emerg}' not emergency", f"got: {answer[:50]}")
        fail_count += 1

# TEST 7: DISCLAIMER ENFORCEMENT
test_section("DISCLAIMER & SAFETY")

queries = [
    "I have a fever",
    "Should I see a doctor?",
    "Thanks for helping",
]

all_have_disclaimer = True
for q in queries:
    result = service.chat_answer(q)
    answer = result["answer"]
    
    if "healthcare professional" not in answer and "consult" not in answer:
        test_fail(f"'{q}' missing disclaimer")
        all_have_disclaimer = False
        fail_count += 1

if all_have_disclaimer:
    test_pass("All responses include healthcare disclaimer (100%)")
    pass_count += 3

# TEST 8: RESPONSE FORMAT
test_section("RESPONSE FORMAT COMPLIANCE")

queries = ["I have fever", "Should I see doctor?", "What helps?"]
format_ok = True

for q in queries:
    result = service.chat_answer(q)
    answer = result["answer"]
    
    sentences = answer.count('.') + answer.count('!') + answer.count('?')
    if sentences < 2 or sentences > 4:
        test_fail(f"'{q}' has {sentences} sentences (expected 2-4)")
        format_ok = False
        fail_count += 1

if format_ok:
    test_pass("All responses are 2-3 sentences")
    pass_count += 1

# FINAL SUMMARY
print("\n" + "="*70)
print("[SUMMARY]")
print("="*70)
print(f"Passed: {pass_count}")
print(f"Failed: {fail_count}")
print(f"Total:  {pass_count + fail_count}")

if fail_count == 0:
    print("\n[SUCCESS] ALL OPTIMIZATIONS VALIDATED!")
    print("  [OK] System is fast, accurate, and safe")
    print("  [OK] Temperature/duration parsing working")
    print("  [OK] Emergency detection active")
    print("  [OK] Responses are context-aware")
    print("  [OK] All disclaimers included")
    sys.exit(0)
else:
    print(f"\n[ERROR] {fail_count} test(s) failed")
    sys.exit(1)
