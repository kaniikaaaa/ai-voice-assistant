"""Test voice output (text-to-speech)"""
print("Testing Text-to-Speech...")
print("="*50)

try:
    from speech import speak, init_engine
    
    print("\n[TEST 1] Initializing TTS engine...")
    engine = init_engine()
    
    if engine:
        print("[OK] TTS engine initialized!")
        
        print("\n[TEST 2] Testing voice output...")
        print("You should hear: 'Hello! This is a test of the voice system.'")
        speak("Hello! This is a test of the voice system.")
        
        print("\n[TEST 3] Testing with longer text...")
        print("You should hear a longer sentence...")
        speak("The AI assistant is working properly. If you can hear this, the voice output is functioning correctly.")
        
        print("\n[SUCCESS] Voice test complete!")
        print("If you heard the voice, TTS is working!")
        print("\nIf you did NOT hear anything:")
        print("1. Check your speakers/headphones are connected")
        print("2. Check Windows volume is not muted")
        print("3. Check if other apps can play sound")
    else:
        print("[ERROR] Could not initialize TTS engine!")
        
except Exception as e:
    print(f"[ERROR] Voice test failed: {e}")
    import traceback
    traceback.print_exc()
