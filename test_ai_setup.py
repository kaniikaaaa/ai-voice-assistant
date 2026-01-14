"""
AI Assistant Zen - Setup Test Script
Run this to verify your AI configuration is working
"""
import os
import sys
from dotenv import load_dotenv

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("AI ASSISTANT ZEN - SETUP TEST")
print("="*60)

# Load environment variables
load_dotenv()

# Test 1: Check if .env file exists
print("\n[TEST 1] Checking .env file...")
if os.path.exists('.env'):
    print("✓ .env file found")
else:
    print("✗ .env file NOT found")
    print("  → Create a .env file with your API keys")
    print("  → See SETUP_API_KEYS.txt for instructions")

# Test 2: Check API keys
print("\n[TEST 2] Checking API keys...")
openai_key = os.getenv('OPENAI_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

if openai_key:
    masked_key = openai_key[:10] + "..." + openai_key[-4:] if len(openai_key) > 14 else "***"
    print(f"✓ OpenAI API key found: {masked_key}")
else:
    print("○ OpenAI API key not found (optional but recommended)")

if gemini_key:
    masked_key = gemini_key[:10] + "..." + gemini_key[-4:] if len(gemini_key) > 14 else "***"
    print(f"✓ Gemini API key found: {masked_key}")
else:
    print("○ Gemini API key not found (optional)")

if not openai_key and not gemini_key:
    print("\n⚠️  WARNING: No AI keys found!")
    print("   You need at least ONE API key for AI responses")
    print("   Get keys from:")
    print("   - OpenAI: https://platform.openai.com/api-keys")
    print("   - Gemini: https://makersuite.google.com/app/apikey")

# Test 3: Check dependencies
print("\n[TEST 3] Checking dependencies...")
required_packages = [
    'pyttsx3',
    'speech_recognition',
    'customtkinter',
    'python-dotenv',
    'openai',
    'google.generativeai'
]

missing_packages = []

for package in required_packages:
    try:
        if package == 'python-dotenv':
            import dotenv
        elif package == 'speech_recognition':
            import speech_recognition
        elif package == 'google.generativeai':
            from google import genai
        else:
            __import__(package.replace('-', '_'))
        print(f"✓ {package} installed")
    except ImportError:
        print(f"✗ {package} NOT installed")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    print(f"   Install with: pip install {' '.join(missing_packages)}")

# Test 4: Test OpenAI connection (if key exists)
if openai_key:
    print("\n[TEST 4] Testing OpenAI connection...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        
        print("  Sending test query to ChatGPT...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello! AI is working!' in exactly those words."}
            ],
            max_tokens=20
        )
        
        answer = response.choices[0].message.content.strip()
        print(f"  ChatGPT Response: {answer}")
        print("✓ OpenAI ChatGPT is working perfectly!")
        
    except Exception as e:
        print(f"✗ OpenAI test failed: {e}")
        print("  Check your API key and internet connection")

# Test 5: Test Gemini connection (if key exists)
if gemini_key:
    print("\n[TEST 5] Testing Gemini connection...")
    try:
        from google import genai
        client = genai.Client(api_key=gemini_key)
        
        print("  Sending test query to Gemini...")
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents="Say 'Hello! AI is working!' in exactly those words."
        )
        
        answer = response.text.strip()
        print(f"  Gemini Response: {answer}")
        print("✓ Gemini AI is working perfectly!")
        
    except Exception as e:
        print(f"✗ Gemini test failed: {e}")
        print("  Check your API key and internet connection")

# Final summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)

if (openai_key or gemini_key) and not missing_packages:
    print("✓ Your assistant is ready to use!")
    print("  Run: python main.py")
else:
    print("⚠️  Setup incomplete. Please fix the issues above.")
    print("  See SETUP_API_KEYS.txt for detailed instructions")

print("="*60)
input("\nPress Enter to exit...")
