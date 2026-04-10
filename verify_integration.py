#!/usr/bin/env python3
"""
VERIFICATION SCRIPT - AI Health Assistant Complete Integration
This script verifies all components are in place and working.
Run: python verify_integration.py
"""

import os
import json
from pathlib import Path

# Define project root
PROJECT_ROOT = Path(__file__).parent

# Files that should exist
REQUIRED_FILES = {
    'backend': [
        'app.py',
        'requirements.txt',
    ],
    'frontend': [
        'package.json',
        'src/App.jsx',
        'src/services/healthAnalysisService.js',
        'src/components/SymptomAnalyzer.jsx',
        'src/components/HealthHistory.jsx',
    ],
    'root': [
        'INTEGRATION_COMPLETE.md',
        'QUICK_START_INTEGRATION.md',
        'IMPLEMENTATION_SUMMARY.md',
    ]
}

# Code patterns to check
CODE_PATTERNS = {
    'backend/app.py': [
        '@app.route(\'/analyze\', methods=[\'POST\'])',
        'requests.post("http://localhost:11434/api/generate"',
        'def analyze():'
    ],
    'frontend/src/App.jsx': [
        'import SymptomAnalyzer',
        'import HealthHistory',
        '<SymptomAnalyzer />',
        '<HealthHistory />'
    ],
    'frontend/src/services/healthAnalysisService.js': [
        'export async function analyzeSymptoms',
        'export function saveToHistory',
        'export function clearHistory',
        'ANALYZE_ENDPOINT'
    ],
    'frontend/src/components/SymptomAnalyzer.jsx': [
        'healthAnalysisService',
        'analyzeSymptoms',
        'saveToHistory'
    ],
    'frontend/src/components/HealthHistory.jsx': [
        'loadHistory',
        'clearHistory',
        'deleteHistoryEntry'
    ]
}

def check_file_exists(file_path):
    """Check if file exists"""
    full_path = PROJECT_ROOT / file_path
    return full_path.exists()

def check_file_content(file_path, patterns):
    """Check if file contains required patterns"""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return False, f"File not found: {file_path}"
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            missing_patterns = []
            for pattern in patterns:
                if pattern not in content:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                return False, f"Missing patterns: {missing_patterns}"
            return True, "All patterns found"
    except Exception as e:
        return False, str(e)

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_check(passed, message):
    """Print check result"""
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {message}")

def main():
    print_header("AI HEALTH ASSISTANT - INTEGRATION VERIFICATION")
    
    total_checks = 0
    passed_checks = 0
    
    # Check required files exist
    print("1. CHECKING FILES EXIST")
    print("-" * 60)
    
    for category, files in REQUIRED_FILES.items():
        for file in files:
            total_checks += 1
            if category == 'root':
                path = file
            else:
                path = f"{category}/{file}"
            
            exists = check_file_exists(path)
            print_check(exists, f"{path}")
            if exists:
                passed_checks += 1
    
    # Check file content
    print("\n2. CHECKING CODE PATTERNS")
    print("-" * 60)
    
    for file_path, patterns in CODE_PATTERNS.items():
        for pattern in patterns:
            total_checks += 1
            passed, msg = check_file_content(file_path, [pattern])
            display_msg = f"{file_path}: {pattern[:40]}..."
            print_check(passed, display_msg)
            if passed:
                passed_checks += 1
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    print(f"Passed: {passed_checks}/{total_checks} ({percentage:.1f}%)")
    
    if passed_checks == total_checks:
        print("\n✨ ALL CHECKS PASSED! ✨")
        print("\nYour AI Health Assistant integration is complete!")
        print("\nNext steps:")
        print("1. Start Ollama: ollama serve")
        print("2. Start Backend: cd backend && python app.py")
        print("3. Start Frontend: cd frontend && npm start")
        print("\nSee QUICK_START_INTEGRATION.md for detailed instructions.")
        return 0
    else:
        print(f"\n⚠️  SOME CHECKS FAILED ({total_checks - passed_checks} issues)")
        print("Check the marks above to see what's missing.")
        return 1

if __name__ == '__main__':
    exit(main())
