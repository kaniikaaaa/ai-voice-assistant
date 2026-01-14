# 📁 core/speech.py
import pyttsx3
import speech_recognition as sr

engine = None

def init_engine():
    global engine
    try:
        print("🔧 Initializing text-to-speech engine...")
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Try to set a female voice, otherwise use default
        for voice in voices:
            if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'girl', 'zira']):
                engine.setProperty('voice', voice.id)
                print(f"✓ Voice set: {voice.name}")
                break
        
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        print("✓ Text-to-speech engine ready!")
        return engine
    except Exception as e:
        print(f"❌ TTS init error: {e}")
        return None

def speak(text):
    global engine
    if not engine:
        engine = init_engine()
    
    if not engine:
        print(f"⚠️ TTS not available. Text output: {text}")
        return
    
    try:
        print(f"🔊 Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        print("✓ Speech completed")
    except Exception as e:
        print(f"❌ Speech error: {e}")
        # Try to reinitialize engine
        engine = None
        engine = init_engine()
        if engine:
            try:
                engine.say(text)
                engine.runAndWait()
            except:
                print(f"⚠️ TTS failed. Text: {text}")

def listen():
    r = sr.Recognizer()
    
    # Adjust recognizer settings for better performance
    r.energy_threshold = 300  # Minimum audio energy to consider for recording
    r.dynamic_energy_threshold = True  # Automatically adjust to ambient noise
    r.pause_threshold = 0.8  # Seconds of silence to consider end of phrase
    
    try:
        with sr.Microphone() as source:
            print("\n🎧 Listening... (speak now)")
            
            # Adjust for ambient noise
            print("🔧 Adjusting for background noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            # Listen with longer timeout and phrase limit
            print("👂 Ready - speak your command...")
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
            
            print("🔄 Processing speech...")
            text = r.recognize_google(audio)
            print(f"✓ Recognized: '{text}'\n")
            return text
            
    except sr.WaitTimeoutError:
        print("⏱️ Timeout - no speech detected (waited 10 seconds)")
        return ""
    except sr.UnknownValueError:
        print("❓ Could not understand audio - please speak clearly")
        return ""
    except sr.RequestError as e:
        print(f"❌ Network error: {e}")
        print("⚠️ Check your internet connection")
        return ""
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return ""
