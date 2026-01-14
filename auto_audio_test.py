"""
Automatic audio test - tests all 3 voices
"""
import pyttsx3
import time

print("="*60)
print("AUTOMATIC AUDIO TEST")
print("="*60)
print("\nThis will test all 3 voices automatically.")
print("Listen carefully for 3 different voices speaking.")
print("\nStarting in 2 seconds...")
time.sleep(2)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

print(f"\nFound {len(voices)} voices. Testing each one...\n")

for i, voice in enumerate(voices):
    print(f"\n[VOICE {i+1}] {voice.name}")
    print("-" * 60)
    
    engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    text = f"This is voice number {i+1}. Testing audio output."
    
    print(f"Speaking: '{text}'")
    print("[LISTEN NOW...]")
    
    engine.say(text)
    engine.runAndWait()
    
    print("[OK] Voice test completed")
    time.sleep(1)

print("\n" + "="*60)
print("ALL VOICES TESTED")
print("="*60)
print("\nDid you hear ANY of the 3 voices?")
print("\nYES → One of the voices works! Audio system OK!")
print("      Check which voice you heard best.")
print("\nNO  → Windows audio routing problem!")
print("      Solutions:")
print("      1. Check Volume Mixer (Python not muted?)")
print("      2. Check Sound Settings (Correct output?)")
print("      3. Read: FIX_AUDIO_NOW.txt")
print("\n" + "="*60)
