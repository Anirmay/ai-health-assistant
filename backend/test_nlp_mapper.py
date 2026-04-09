"""
NLP Symptom Mapper - Demo & Testing
Shows how the system understands natural language symptom inputs
"""

from ml_models.symptom_mapper import SymptomMapper, map_user_symptoms, get_symptom_mapping_summary

# Initialize the mapper
mapper = SymptomMapper()

print("=" * 70)
print("🧠 NLP SYMPTOM MAPPER - DEMO")
print("=" * 70)
print()

# Test cases: Show how NLP understands different inputs
test_inputs = [
    "hairfall",
    "head pain",
    "feeling tired",
    "my head is throbbing",
    "can't sleep",
    "throwing up",
    "tummy ache",
    "difficulty breathing",
    "severe headache",
    "loss of hair",
    "feverish",
    "runny nose",
    "sore chest",
    "weak and exhausted",
]

print("📝 TESTING NLP MAPPINGS:\n")

for user_input in test_inputs:
    # Single symptom mapping
    result = mapper.map_symptom(user_input)
    
    print(f"Input: \"{user_input}\"")
    print(f"  ↓ Mapped to: \"{result['mapped_symptom']}\"")
    print(f"  ✓ Confidence: {int(result['confidence'] * 100)}% ({result['method']})")
    
    if result['alternatives']:
        print(f"  📌 Alternatives:")
        for alt in result['alternatives']:
            print(f"     - {alt['symptom']} ({int(alt['confidence'] * 100)}%)")
    print()

print("=" * 70)
print("🔬 TESTING MULTIPLE SYMPTOMS:\n")

# Test multiple symptoms at once
multi_symptom_inputs = [
    "fever, cough, headache",
    "hairfall and exhaustion",
    "difficulty breathing with chest pain",
    "feeling nauseous and dizzy",
]

for user_input in multi_symptom_inputs:
    mappings = map_user_symptoms(user_input)
    summary, confidence, mapped = get_symptom_mapping_summary(mappings)
    
    print(f"Input: \"{user_input}\"")
    print(f"Mapping Summary:")
    print(summary)
    print(f"Overall Confidence: {int(confidence * 100)}%")
    print(f"Mapped Symptoms: {', '.join(mapped)}")
    print()

print("=" * 70)
print("✅ NLP Mapping Demo Complete!")
print("=" * 70)
print()
print("Key Features:")
print("  ✓ Understands synonyms (hairfall → hair loss)")
print("  ✓ Handles variations (feverish → fever)")
print("  ✓ Processes multiple symptoms")
print("  ✓ Returns confidence scores")
print("  ✓ Falls back to fuzzy matching if needed")
print("  ✓ Fast & lightweight (uses all-MiniLM-L6-v2 model)")
print()
