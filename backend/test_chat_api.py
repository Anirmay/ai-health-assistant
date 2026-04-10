"""
Test script for AI Health Assistant Chat API
Tests all endpoints and provides examples of API usage.
"""

import requests
import json
import time
from typing import Dict, List

BASE_URL = "http://localhost:5000"

class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def print_test_request(method: str, endpoint: str, data: Dict = None):
    """Print test request details."""
    url = f"{BASE_URL}{endpoint}"
    print(f"{Colors.YELLOW}📨 {method} {url}{Colors.END}")
    if data:
        print(f"   Body: {json.dumps(data, indent=2)}")

def print_response(response: Dict, response_time: float = None):
    """Print formatted response."""
    print(f"\n📋 Response:")
    print(json.dumps(response, indent=2))
    if response_time:
        print(f"⏱️  Response time: {response_time:.2f}s")

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_health_check():
    """Test /api/health endpoint."""
    print_header("Test 1: Health Check")
    
    try:
        print_test_request("GET", "/api/health")
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        data = response.json()
        
        print_response(data)
        print_success(f"API is healthy: {data.get('status')}")
        return True
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_status():
    """Test /api/status endpoint."""
    print_header("Test 2: Service Status")
    
    try:
        print_test_request("GET", "/api/status")
        response = requests.get(f"{BASE_URL}/api/status", timeout=5)
        data = response.json()
        
        print_response(data)
        if data.get('ollama') == 'online':
            print_success("Ollama service is online")
        else:
            print_error("Ollama service is offline - start it with: ollama serve")
        return data.get('ollama') == 'online'
    except Exception as e:
        print_error(f"Status check failed: {str(e)}")
        return False

def test_config():
    """Test /api/config endpoint."""
    print_header("Test 3: Configuration (Debug)")
    
    try:
        print_test_request("GET", "/api/config")
        response = requests.get(f"{BASE_URL}/api/config", timeout=5)
        data = response.json()
        
        print_response(data)
        print_success("Configuration retrieved")
        return True
    except Exception as e:
        print_error(f"Config check failed: {str(e)}")
        return False

def test_chat_basic():
    """Test /api/chat endpoint with basic questions."""
    print_header("Test 4: Chat - Basic Questions")
    
    test_questions = [
        "I have a fever and cough",
        "How long does the flu last?",
        "Should I see a doctor?",
        "What can I do for a headache?"
    ]
    
    success_count = 0
    total_time = 0
    
    for question in test_questions:
        try:
            print_test_request("POST", "/api/chat", {"message": question})
            
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={"message": question},
                headers={"Content-Type": "application/json"},
                timeout=40
            )
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            
            data = response.json()
            
            # Print response summary
            reply = data.get('reply', '')
            status = data.get('status', '')
            
            print(f"\n📋 Response ({status}):")
            print(f"   {reply[:150]}..." if len(reply) > 150 else f"   {reply}")
            print(f"⏱️  Response time: {elapsed_time:.2f}s")
            
            if status == 'success' and reply:
                print_success(f"Received response: {len(reply)} chars")
                success_count += 1
            else:
                print_error(f"No valid response: {data}")
            
            print()
        except requests.exceptions.Timeout:
            print_error(f"Request timeout for: {question}")
        except Exception as e:
            print_error(f"Chat failed for '{question}': {str(e)}")
    
    if success_count > 0:
        avg_time = total_time / success_count
        print_success(f"Chat tests: {success_count}/{len(test_questions)} successful")
        print_info(f"Average response time: {avg_time:.2f}s")
    
    return success_count == len(test_questions)

def test_chat_edge_cases():
    """Test /api/chat with edge cases."""
    print_header("Test 5: Chat - Edge Cases")
    
    test_cases = [
        ("", "empty message"),
        ("123", "numbers only"),
        ("!@#$%", "special characters"),
        ("a" * 500, "very long message"),
    ]
    
    for message, description in test_cases:
        try:
            print_test_request("POST", "/api/chat", {"message": message})
            print(f"   Testing: {description}")
            
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            data = response.json()
            status = data.get('status')
            
            if status == 'error':
                print_success(f"Correctly handled error case: {status}")
            else:
                print_info(f"Got response with status: {status}")
            print()
        except Exception as e:
            print_error(f"Test failed for '{description}': {str(e)}")

def test_stats():
    """Test /api/stats endpoint."""
    print_header("Test 6: Service Statistics")
    
    try:
        print_test_request("GET", "/api/stats")
        response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
        data = response.json()
        
        print_response(data)
        stats = data.get('stats', {})
        success_rate = stats.get('success_rate', 'N/A')
        print_success(f"API Success rate: {success_rate}")
        return True
    except Exception as e:
        print_error(f"Stats check failed: {str(e)}")
        return False

def test_invalid_request():
    """Test error handling for invalid requests."""
    print_header("Test 7: Error Handling - Invalid Request")
    
    try:
        print_test_request("POST", "/api/chat", None)
        print("   Testing: No JSON body")
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        data = response.json()
        error = data.get('error', '')
        
        if data.get('status') == 'error':
            print_success(f"Correctly handled invalid request: {error}")
        else:
            print_error("Should have returned error status")
        
        print_response(data)
        return True
    except Exception as e:
        print_error(f"Invalid request test failed: {str(e)}")
        return False

def test_cors():
    """Test CORS support."""
    print_header("Test 8: CORS Support")
    
    try:
        print_test_request("OPTIONS", "/api/chat")
        response = requests.options(
            f"{BASE_URL}/api/chat",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
        
        cors_header = response.headers.get('Access-Control-Allow-Origin', 'Not set')
        print(f"\n📋 CORS Headers:")
        print(f"   Access-Control-Allow-Origin: {cors_header}")
        
        if cors_header:
            print_success("CORS is enabled")
        else:
            print_info("CORS might be handled differently")
        return True
    except Exception as e:
        print_error(f"CORS test failed: {str(e)}")
        return False

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and provide summary."""
    print(f"\n{Colors.CYAN}")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🏥 AI Health Assistant API - Test Suite".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print(Colors.END)
    
    print_info(f"API Base URL: {BASE_URL}")
    print_info("Make sure Ollama is running: ollama serve")
    
    tests = [
        ("Health Check", test_health_check),
        ("Service Status", test_status),
        ("Configuration", test_config),
        ("Chat - Basic", test_chat_basic),
        ("Chat - Edge Cases", test_chat_edge_cases),
        ("Statistics", test_stats),
        ("Error Handling", test_invalid_request),
        ("CORS Support", test_cors),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Unexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print_header("📊 Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"{'Test Name':<25} {'Status':<10}")
    print("─" * 35)
    for test_name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{test_name:<25} {status}")
    
    print("─" * 35)
    percentage = (passed / total * 100) if total > 0 else 0
    print(f"Total: {passed}/{total} passed ({percentage:.0f}%)\n")
    
    if passed == total:
        print_success("All tests passed! API is working correctly. 🎉")
    else:
        print_error(f"{total - passed} test(s) failed. Check configuration and logs.")
    
    return passed == total

if __name__ == "__main__":
    import sys
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
