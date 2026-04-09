#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI Health Assistant Optimizations
Tests: Speed, Accuracy, Context Awareness, and Safety
"""

import sys
import time
import unittest
from typing import Dict
from ai_module.ollama_service import OllamaService

class TestOptimizations(unittest.TestCase):
    """Test optimizations: speed, accuracy, context, safety."""
    
    def setUp(self):
        """Initialize service for testing."""
        self.service = OllamaService()
        self.start_time = None
    
    def _measure_time(self, func, *args):
        """Measure execution time."""
        self.start_time = time.time()
        result = func(*args)
        elapsed = time.time() - self.start_time
        return result, elapsed
    
    def _print_test(self, name: str, passed: bool, details: str = ""):
        """Print test result."""
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {name} {details}")
        return passed
    
    # ========== SPEED TESTS ==========
    def test_01_predefined_response_speed(self):
        """Test 1: Predefined responses return in <100ms (instant)."""
        question = "How long does a fever take to recover?"
        result, elapsed = self._measure_time(
            self.service.chat_answer,
            question
        )
        
        passed = elapsed < 0.1  # 100ms
        self._print_test(
            "Predefined Response Speed",
            passed,
            f"({elapsed*1000:.1f}ms)"
        )
        self.assertLess(elapsed, 0.1, f"Too slow: {elapsed}s")
    
    def test_02_recovery_time_predefined(self):
        """Test 2: Common recovery time question gets instant answer."""
        questions = [
            "How long will my fever last?",
            "How much time for recovery?",
            "When will I get better?"
        ]
        
        for q in questions:
            result, elapsed = self._measure_time(
                self.service.chat_answer,
                q
            )
            self.assertLess(elapsed, 0.1, f"Predefined response too slow: {elapsed}s")
            self.assertIn("day", result["answer"].lower())
        
        self._print_test("Recovery Time Questions", True, "(all instant)")
    
    def test_03_doctor_question_predefined(self):
        """Test 3: 'Should I see a doctor' question gets instant answer."""
        questions = [
            "Should I see a doctor?",
            "Do I need to visit a doctor?", 
            "When to see a doctor?"
        ]
        
        for q in questions:
            result, elapsed = self._measure_time(
                self.service.chat_answer,
                q
            )
            self.assertLess(elapsed, 0.1)
            self.assertIn("doctor", result["answer"].lower())
        
        self._print_test("Doctor Question Predefined", True)
    
    # ========== ACCURACY TESTS ==========
    def test_04_no_diagnosis_in_answer(self):
        """Test 4: Response never gives diagnosis."""
        response = "You have diabetes and should take insulin."
        
        invalid = self.service._is_invalid_response(response)
        passed = invalid  # Should be flagged as invalid
        
        self._print_test("Diagnosis Detection", passed)
        self.assertTrue(invalid)
    
    def test_05_no_medicine_prescription(self):
        """Test 5: Response never prescribes medicine."""
        responses = [
            "I prescribe this medicine",
            "Take this pill twice daily",
            "Buy this medication",
            "Use this drug for relief"
        ]
        
        for resp in responses:
            invalid = self.service._is_invalid_response(resp)
            self.assertTrue(invalid, f"Missed prescription detection: {resp}")
        
        self._print_test("Prescription Detection", True, f"({len(responses)} patterns)")
    
    def test_06_no_overconfidence(self):
        """Test 6: Response never claims certainty."""
        responses = [
            "You definitely have the flu",
            "This is 100% a bacterial infection",
            "The cause is certainly stress"
        ]
        
        for resp in responses:
            invalid = self.service._is_invalid_response(resp)
            self.assertTrue(invalid)
        
        self._print_test("Overconfidence Detection", True)
    
    def test_07_temperature_specific_response(self):
        """Test 7: Response mentions specific temperature."""
        result = self.service._handle_fever_question("I have 104F fever")
        answer = result["answer"].lower()
        
        # Should mention the specific temp or indicate it's high
        has_temp = "104" in answer or "high" in answer or "concerning" in answer
        
        passed = has_temp
        self._print_test("Temperature-Specific Response", passed)
        self.assertTrue(has_temp, f"Temperature not mentioned: {answer}")
    
    def test_08_duration_aware_response(self):
        """Test 8: Response acknowledges symptom duration."""
        result = self.service._handle_fever_question("Fever for a week")
        answer = result["answer"].lower()
        
        # Should mention duration or recommend doctor
        has_context = "week" in answer or "doctor" in answer or "evaluation" in answer
        
        passed = has_context
        self._print_test("Duration-Aware Response", passed)
        self.assertTrue(has_context)
    
    def test_09_no_random_calculations(self):
        """Test 9: Response doesn't contain random math."""
        response = "2 + 2 = 4 so your fever is bad"
        
        invalid = self.service._is_invalid_response(response)
        passed = invalid  # Should be flagged
        
        self._print_test("Random Math Detection", passed)
        self.assertTrue(invalid)
    
    def test_10_response_format_compliance(self):
        """Test 10: All responses are 2-3 sentences."""
        questions = [
            "I have a headache",
            "Should I see a doctor?",
            "What's recovery time?"
        ]
        
        all_pass = True
        for q in questions:
            result = self.service.chat_answer(q)
            answer = result["answer"]
            
            # Count sentences (rough)
            sentence_count = answer.count('.') + answer.count('!') + answer.count('?')
            
            # Should be 2-4 sentences (accounting for disclaimer)
            if sentence_count < 2 or sentence_count > 4:
                all_pass = False
                print(f"  [FAIL] Wrong format for '{q}': {sentence_count} sentences")
        
        self._print_test("Response Format Compliance", all_pass)
        self.assertTrue(all_pass)
    
    # ========== CONTEXT AWARENESS TESTS ==========
    def test_11_context_history_support(self):
        """Test 11: Context history can be passed and used."""
        history = [
            {"question": "I have a fever", "answer": "..."},
            {"question": "How high is my fever?", "answer": "..."}
        ]
        
        result = self.service.chat_answer(
            "What should I do?",
            history=history
        )
        
        # Should return a valid response considering the context
        passed = bool(result.get("answer")) and len(result["answer"]) > 20
        
        self._print_test("Context History Support", passed)
        self.assertTrue(passed)
    
    def test_12_polite_response_handling(self):
        """Test 12: Polite phrases handled gracefully."""
        polite_phrases = ["Thanks!", "Thank you", "Appreciate your help"]
        
        for phrase in polite_phrases:
            result = self.service.chat_answer(phrase)
            
            # Should have a welcome response, not error
            self.assertIn("welcome", result["answer"].lower())
            self.assertIn("healthcare professional", result["answer"])
        
        self._print_test("Polite Response Handling", True)
    
    def test_13_emergency_priority(self):
        """Test 13: Emergency symptoms get immediate routing."""
        emergencies = [
            "I can't breathe",
            "Severe chest pain",
            "I'm unconscious - help!",
            "Bleeding heavily"
        ]
        
        for emergency in emergencies:
            result = self.service.chat_answer(emergency)
            answer = result["answer"].lower()
            
            # Should mention immediate/emergency
            has_emergency_response = "immediately" in answer or "emergency" in answer or "call" in answer
            self.assertTrue(has_emergency_response, f"Missed emergency: {emergency}")
        
        self._print_test("Emergency Priority Routing", True, f"({len(emergencies)} cases)")
    
    # ========== SAFETY TESTS ==========
    def test_14_always_includes_disclaimer(self):
        """Test 14: EVERY response includes healthcare disclaimer."""
        questions = [
            "Hi",
            "Thanks",
            "I have fever",
            "Should I see a doctor?"
        ]
        
        for q in questions:
            result = self.service.chat_answer(q)
            answer = result["answer"]
            
            # Must include disclaimer
            has_disclaimer = "healthcare professional" in answer or "consult" in answer
            self.assertTrue(has_disclaimer, f"Missing disclaimer in: {q}")
        
        self._print_test("Disclaimer Enforcement", True, "(100% coverage)")
    
    def test_15_invalid_response_detection(self):
        """Test 15: System detects and rejects invalid responses."""
        invalid_responses = [
            "You have diabetes",
            "Take ibuprofen 400mg twice daily",
            "This is definitely a viral infection",
            "I prescribe antibiotics",
            "x = 2 + 3 is your health score"
        ]
        
        for resp in invalid_responses:
            is_invalid = self.service._is_invalid_response(resp)
            self.assertTrue(is_invalid, f"Failed to catch invalid: {resp}")
        
        self._print_test("Invalid Response Detection", True, f"({len(invalid_responses)} patterns)")
    
    # ========== TEMPERATURE PARSING TESTS ==========
    def test_16_temperature_parsing_fahrenheit(self):
        """Test 16: Parses Fahrenheit temperatures."""
        tests = [
            ("I have 101F fever", 101.0),
            ("temperature is 104.5F", 104.5),
            ("I have 99.5 degrees", 99.5),
            ("101 fahrenheit", 101.0),
        ]
        
        for text, expected in tests:
            temp = self.service._extract_temperature(text)
            self.assertIsNotNone(temp)
            self.assertAlmostEqual(temp, expected, places=1)
        
        self._print_test("Fahrenheit Parsing", True, f"({len(tests)} formats)")
    
    def test_17_temperature_parsing_celsius(self):
        """Test 17: Parses and converts Celsius temperatures."""
        tests = [
            ("I have 39.2C", 102.56),  # 39.2*9/5+32 = 102.56
            ("Temperature is 38C", 100.4),  # 38*9/5+32 = 100.4
            ("39 degrees celsius", 102.2),
        ]
        
        for text, expected in tests:
            temp = self.service._extract_temperature(text)
            self.assertIsNotNone(temp)
            self.assertAlmostEqual(temp, expected, places=0)
        
        self._print_test("Celsius Parsing + Conversion", True, f"({len(tests)} formats)")
    
    # ========== DURATION PARSING TESTS ==========
    def test_18_duration_extraction(self):
        """Test 18: Extracts symptom durations correctly."""
        tests = [
            ("fever for a week", "about a week"),
            ("symptoms for a month", "over a month"),
            ("started today", "today"),
            ("been sick for 3 days", "three days"),
        ]
        
        for text, expected_contains in tests:
            duration = self.service._extract_duration(text)
            self.assertIsNotNone(duration)
            # Check if expected content is in the duration
            self.assertTrue(
                any(w in duration.lower() for w in expected_contains.split()),
                f"Expected '{expected_contains}' in '{duration}'"
            )
        
        self._print_test("Duration Extraction", True, f"({len(tests)} formats)")
    
    # ========== INTEGRATION TESTS ==========
    def test_19_fever_low_high_different_responses(self):
        """Test 19: Low fever vs high fever get different responses."""
        low = self.service._handle_fever_question("I have 99F fever")
        high = self.service._handle_fever_question("I have 104F fever")
        
        low_answer = low["answer"].lower()
        high_answer = high["answer"].lower()
        
        # Should be visibly different
        different = low_answer != high_answer
        
        # High should mention urgency
        high_has_urgency = "high" in high_answer or "urgent" in high_answer or "soon" in high_answer
        
        passed = different and high_has_urgency
        self._print_test("Fever Severity Differentiation", passed)
        self.assertTrue(passed)
    
    def test_20_system_status_and_config(self):
        """Test 20: System reports correct configuration."""
        status = self.service.get_system_status()
        
        # Check config
        self.assertEqual(status["model"], "phi3")
        self.assertIn("phi3", status["mode"])
        
        # Check response format
        result = self.service.chat_answer("Hi")
        self.assertIn("answer", result)
        self.assertIn("follow_up_suggestions", result)
        self.assertIn("disclaimer", result)
        
        self._print_test("System Status & Config", True)


def print_summary():
    """Print test summary."""
    print("\n" + "="*60)
    print("[*] AI HEALTH ASSISTANT - OPTIMIZATION TEST SUITE")
    print("="*60)
    print("\n[TESTS INCLUDE]:")
    print("  [OK] Speed (predefined responses <100ms)")
    print("  [OK] Accuracy (no diagnosis, prescriptions, etc.)")
    print("  [OK] Context Awareness (history support)")
    print("  [OK] Safety (disclaimers, emergency routing)")
    print("  [OK] Format Compliance (2-3 sentences)")
    print("  [OK] Temperature Parsing (F, C, conversions)")
    print("  [OK] Duration Extraction (days, weeks, months)")
    print("\n[RUNNING] 20 comprehensive tests...\n")


if __name__ == "__main__":
    print_summary()
    
    # Run tests with verbose output
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestOptimizations)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print final summary
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("[SUCCESS] ALL TESTS PASSED!")
        print(f"Total: {result.testsRun} tests")
        print("\n[RESULT] System is optimized, accurate, and safe!")
    else:
        print("[ERROR] SOME TESTS FAILED")
        print(f"Failed: {len(result.failures)} | Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    # Exit with status
    sys.exit(0 if result.wasSuccessful() else 1)
