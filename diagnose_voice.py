"""Complete voice system diagnostic"""
import sys

print("="*60)
print("AI ASSISTANT - VOICE DIAGNOSTIC")
print("="*60)

# Test 1: Import pyttsx3
print("\n[TEST 1] Checking pyttsx3 installation...")
try:
    import pyttsx3
    print("[OK] pyttsx3 is installed")
except ImportError:
    print("[ERROR] pyttsx3 not installed!")
    print("[FIX] Run: pip install pyttsx3")
    sys.exit(1)

# Test 2: Initialize engine
print("\n[TEST 2] Initializing TTS engine...")
try:
    engine = pyttsx3.init()
    print("[OK] TTS engine initialized")
except Exception as e:
    print(f"[ERROR] TTS init failed: {e}")
    print("[FIX] Try reinstalling: pip uninstall pyttsx3 && pip install pyttsx3")
    sys.exit(1)

# Test 3: Get voices
print("\n[TEST 3] Checking available voices...")
try:
    voices = engine.getProperty('voices')
    print(f"[OK] Found {len(voices)} voices:")
    for i, voice in enumerate(voices):
        print(f"  {i+1}. {voice.name} (ID: {voice.id})")
except Exception as e:
    print(f"[ERROR] Could not get voices: {e}")

# Test 4: Test speech output
print("\n[TEST 4] Testing voice output...")
print("="*60)
print("YOU SHOULD HEAR: 'Hello, this is a test of the voice system'")
print("="*60)
input("Press Enter to start voice test...")

try:
    engine.say("Hello, this is a test of the voice system")
    engine.runAndWait()
    print("[OK] Voice output completed!")
    
    print("\n" + "="*60)
    heard = input("Did you HEAR the voice? (yes/no): ").strip().lower()
    
    if heard in ['yes', 'y']:
        print("\n[SUCCESS] ✓ Voice system is working!")
        print("[INFO] Your assistant should work fine.")
        print("[ACTION] Run: python assistant_core.py")
    else:
        print("\n[PROBLEM] Voice output not working")
        print("\n[TROUBLESHOOTING]")
        print("1. Check if speakers/headphones are connected")
        print("2. Check Windows sound settings:")
        print("   - Open 'Sound Settings'")
        print("   - Make sure correct output device is selected")
        print("   - Check volume is not muted")
        print("3. Try different voice:")
        print("   - Edit speech.py")
        print("   - Comment out lines 14-19 (voice selection)")
        print("4. Test with other apps (YouTube, etc.) to verify speakers work")
        print("5. Restart your computer")
        
except Exception as e:
    print(f"[ERROR] Voice test failed: {e}")
    import traceback
    traceback.print_exc()
    print("\n[FIX] Try:")
    print("1. pip uninstall pyttsx3")
    print("2. pip install pyttsx3")
    print("3. Restart computer")

print("\n" + "="*60)
print("Diagnostic complete!")
print("="*60)
