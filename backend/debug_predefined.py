#!/usr/bin/env python3
import time
from ai_module.ollama_service import OllamaService

service = OllamaService()

print("[DEBUG] Testing predefined response speed...")
print("")

# Test message that should trigger predefined response
test_msg = "How long does fever recovery take?"
print(f"Message: '{test_msg}'")
print(f"message_lower: '{test_msg.lower()}'")
print("")

# Check if predefined would match
message_lower = test_msg.lower()
predef = service._get_predefined_response(message_lower)

print(f"Predefined response returned? {predef is not None}")
if predef:
    print(f"Answer: {predef['answer'][:100]}...")
else:
    print("No predefined response (will use LLM or other handler)")

print("")
print("[TIMING] Full chat_answer call:")
start = time.time()
result = service.chat_answer(test_msg)
elapsed = time.time() - start

print(f"Time taken: {elapsed*1000:.0f}ms")
print(f"Answer: {result['answer'][:80]}...")
