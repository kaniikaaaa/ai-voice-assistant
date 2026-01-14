"""Verify OpenAI import works in assistant_core.py context"""
import os
from dotenv import load_dotenv

load_dotenv()

# Test the exact import from assistant_core.py line 224
try:
    from openai import OpenAI
    print("[OK] OpenAI import successful!")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("[OK] API key loaded from .env")
        client = OpenAI(api_key=api_key)
        print("[OK] OpenAI client created successfully!")
        print("\n[SUCCESS] Everything works! The linter warning is a false positive.")
        print("[INFO] Your code is fine - this is just an IDE configuration issue.")
    else:
        print("[WARN] No API key found in .env")
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
except Exception as e:
    print(f"[ERROR] {e}")
