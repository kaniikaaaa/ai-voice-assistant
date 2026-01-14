# Speech module for voice input/output
import pyttsx3
import speech_recognition as sr
import time

engine = None
# Use fresh engine for each speech (more reliable on Windows)
USE_FRESH_ENGINE = True

def init_engine():
    global engine
    try:
        print("[INFO] Initializing text-to-speech engine...")
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Try to set a female voice, otherwise use default
        for voice in voices:
            if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'girl', 'zira']):
                engine.setProperty('voice', voice.id)
                print(f"[OK] Voice set: {voice.name}")
                break
        
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        print("[OK] Text-to-speech engine ready!")
        return engine
    except Exception as e:
        print(f"[ERROR] TTS init error: {e}")
        return None

def speak(text):
    global engine
    
    # Use fresh engine for each speech (more reliable on Windows)
    if USE_FRESH_ENGINE:
        try:
            print(f"[SPEAKING] {text}")
            
            # Create fresh engine
            temp_engine = pyttsx3.init()
            
            # Set voice to Zira (female)
            voices = temp_engine.getProperty('voices')
            for voice in voices:
                if 'zira' in voice.name.lower():
                    temp_engine.setProperty('voice', voice.id)
                    break
            
            # Set properties
            temp_engine.setProperty('rate', 150)
            temp_engine.setProperty('volume', 1.0)
            
            # Speak
            temp_engine.say(text)
            temp_engine.runAndWait()
            
            # Clean up
            del temp_engine
            
            print("[OK] Speech completed")
            time.sleep(0.1)  # Small delay for stability
            return
        except Exception as e:
            print(f"[ERROR] Fresh engine error: {e}")
            # Fall through to old method
    
    # Original method (fallback)
    if not engine:
        engine = init_engine()
    
    if not engine:
        print(f"[WARN] TTS not available. Text output: {text}")
        return
    
    try:
        print(f"[SPEAKING] {text}")
        
        # Clear any pending speech
        engine.stop()
        
        # Add text to queue
        engine.say(text)
        
        # Run and wait - this blocks until speech is done
        engine.runAndWait()
        
        # Extra safety: ensure queue is cleared
        engine.stop()
        
        print("[OK] Speech completed")
    except RuntimeError as e:
        # pyttsx3 sometimes throws RuntimeError on Windows
        print(f"[WARN] Speech engine error: {e}")
        print(f"[INFO] Reinitializing engine...")
        # Force reinitialize
        engine = None
        engine = init_engine()
        if engine:
            try:
                engine.stop()
                engine.say(text)
                engine.runAndWait()
                engine.stop()
                print("[OK] Speech completed (retry)")
            except Exception as e2:
                print(f"[ERROR] TTS retry failed: {e2}")
                print(f"[TEXT] {text}")
    except Exception as e:
        print(f"[ERROR] Speech error: {e}")
        print(f"[TEXT] {text}")

def listen():
    r = sr.Recognizer()
    
    # Adjust recognizer settings for better performance
    r.energy_threshold = 300  # Minimum audio energy to consider for recording
    r.dynamic_energy_threshold = True  # Automatically adjust to ambient noise
    r.pause_threshold = 0.8  # Seconds of silence to consider end of phrase
    
    try:
        with sr.Microphone() as source:
            print("\n[LISTENING] Speak now...")
            
            # Adjust for ambient noise
            print("[INFO] Adjusting for background noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            # Listen with longer timeout and phrase limit
            print("[READY] Speak your command...")
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
            
            print("[PROCESSING] Recognizing speech...")
            text = r.recognize_google(audio)
            print(f"[RECOGNIZED] '{text}'\n")
            return text
            
    except sr.WaitTimeoutError:
        print("[TIMEOUT] No speech detected (waited 10 seconds)")
        return ""
    except sr.UnknownValueError:
        print("[ERROR] Could not understand audio - please speak clearly")
        return ""
    except sr.RequestError as e:
        print(f"[ERROR] Network error: {e}")
        print("[WARN] Check your internet connection")
        return ""
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return ""
