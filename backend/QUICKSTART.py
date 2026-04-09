#!/usr/bin/env python3
"""
QUICK START - Run this to know exactly what to do next
"""

import os
import sys
import subprocess

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AI HEALTH ASSISTANT - QUICK START                        ║
║                                                                              ║
║ Chat not responding? Follow these steps to fix it!                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("📋 CHECKLIST - Complete each step:\n")

print("""
STEP 1: Stop Everything
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If backend is running (Terminal with "localhost:5000"):
  Press: CTRL + C

If Ollama is running (Terminal with "Listening on"):
  Press: CTRL + C
  
Wait 5 seconds for everything to stop.


STEP 2: Start Ollama (MUST BE FIRST)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open a NEW terminal (Terminal 1):

    cd c:\\Users\\HP\\Desktop\\Programming\\AI-Health-Assistant\\ai-health-assistant
    ollama serve

⏳ WAIT until you see:
    Listening on 127.0.0.1:11434

This terminal should STAY OPEN.


STEP 3: Verify gemma:2b Model
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open ANOTHER terminal (Terminal 2):

    ollama list

Check if you see:
    ✅ gemma:2b

If NOT there, run:
    ollama pull gemma:2b

⏳ WAIT for download to complete (might take 5-10 minutes first time)


STEP 4: Start Backend
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open ANOTHER terminal (Terminal 3):

    cd c:\\Users\\HP\\Desktop\\Programming\\AI-Health-Assistant\\ai-health-assistant\\backend
    python app.py

⏳ WAIT until you see:
    ✅ Ollama Service initialized: gemma:2b model, 40s timeout
    ⚠️ Ollama response check passed!
    * Running on http://127.0.0.1:5000


STEP 5: Test Chat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open browser:
    http://localhost:5173

Type: "Hi"

👀 WATCH Terminal 3 (backend) for this output:

    ======================================================================
    🔍 OLLAMA DEBUG - STEP 1: Checking Ollama availability...
       is_available property: True
    
    🔍 OLLAMA DEBUG - STEP 2: Building request...
       Model: gemma:2b
    
    🔍 OLLAMA DEBUG - STEP 3: Sending POST request...
       Timeout: 40 seconds
    
    🔍 OLLAMA DEBUG - STEP 4: Got response!
       Status code: 200
    
    🔍 OLLAMA DEBUG - STEP 5: Parsing JSON response...
       JSON parsed successfully!
    
    ✅ SUCCESS! Got AI response (XX chars)
    ======================================================================

✅ IF YOU SEE THIS: Chat is working! Try "Tell me a joke" or "I have fever"


TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "CANNOT REACH OLLAMA" → Step 2 failed, check ollama serve in Terminal 1

❌ "gemma:2b model NOT FOUND" → Step 3 failed, run: ollama pull gemma:2b

❌ "FLASK NOT RUNNING" → Step 4 failed, check Terminal 3 output

❌ "CONNECTION ERROR" → Ollama crashed, restart Step 2

❌ "TIMEOUT ERROR (40s)" → gemma:2b too slow, give it more time or check RAM

❌ "❌ Response field was EMPTY" → Ollama error, restart Ollama


VERIFY WITH TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In Terminal 3, run:

    python diagnose.py

Should show:
    ✅ Ollama service is RUNNING
    ✅ gemma:2b model is AVAILABLE  
    ✅ Flask backend is RUNNING
    ✅ Got response: ...

If all ✅, run:

    python test_direct_ollama.py

Should show:
    ✅ ALL TESTS PASSED


QUICK TEST WITHOUT BROWSER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In Terminal 4, test API directly:

    curl -X POST http://localhost:5000/api/chat ^
      -H "Content-Type: application/json" ^
      -d {"message":"Hi"}

(On Windows use: curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d "{\"message\":\"Hi\"}")

Should return JSON with real AI response.


EXPECTED CHAT RESPONSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Message: "Hi"
Response: "Hello! How can I help you today?"

Message: "Tell me a joke"  
Response: "Why did the scarecrow win an award? Because he was outstanding in his field!"

Message: "I have fever"
Response: "A fever can indicate infection. Rest, drink fluids, monitor temperature. If over 103°F or lasts 3+ days, see a doctor."


ALL WORKING? 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Congratulations! Your backend is now working!

Keep these terminals open:
  Terminal 1: ollama serve
  Terminal 3: python app.py

Then:
  - Open http://localhost:5173 in browser
  - Chat away! 

For frontend development:
  Terminal 2: cd frontend && npm run dev
  

NEED HELP?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Check BACKEND_RECOVERY_GUIDE.md for detailed troubleshooting

2. Run diagnostics:
   python diagnose.py
   
3. Run direct test:
   python test_direct_ollama.py

4. Copy ALL terminal output and debug output when asking for help
""")

input("\nPress ENTER to continue...")
