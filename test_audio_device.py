"""
Test which audio device pyttsx3 is using
"""
import pyttsx3

print("="*60)
print("AUDIO DEVICE TEST")
print("="*60)

# Method 1: Test with fresh engine
print("\n[TEST 1] Testing TTS with fresh engine...")
engine = pyttsx3.init('sapi5')

# Get all available voices
voices = engine.getProperty('voices')
print(f"\nAvailable voices ({len(voices)}):")
for i, voice in enumerate(voices):
    print(f"  {i+1}. {voice.name}")
    print(f"      ID: {voice.id}")

# Try each voice
print("\n" + "="*60)
print("TESTING EACH VOICE - YOU SHOULD HEAR 3 DIFFERENT VOICES")
print("="*60)

for i, voice in enumerate(voices):
    print(f"\n[TEST] Voice {i+1}: {voice.name}")
    print("You should hear: 'This is voice number [X]'")
    input("Press Enter to test this voice...")
    
    engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    text = f"This is voice number {i+1}. Testing audio output."
    engine.say(text)
    engine.runAndWait()
    
    heard = input("Did you HEAR this voice? (yes/no): ").strip().lower()
    
    if heard in ['yes', 'y']:
        print(f"[SUCCESS] Voice {i+1} works!")
        print(f"\nWorking voice ID: {voice.id}")
        print(f"Voice name: {voice.name}")
        break
    else:
        print(f"[FAILED] Voice {i+1} not heard")
else:
    print("\n[ERROR] None of the voices were heard!")
    print("\n[TROUBLESHOOTING]")
    print("1. Check Windows Sound Settings:")
    print("   - Right-click speaker icon in taskbar")
    print("   - Open Sound Settings")
    print("   - Check 'Output device'")
    print("   - Make sure it's your speakers/headphones")
    print("2. Check volume mixer:")
    print("   - Right-click speaker icon")
    print("   - Open Volume Mixer")
    print("   - Check if Python.exe is muted")
    print("3. Test with other apps (YouTube, etc.)")

del engine
print("\n" + "="*60)
print("Test complete!")
print("="*60)
