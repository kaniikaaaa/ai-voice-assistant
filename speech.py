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
    
    print(f"[SPEAKING] {text}")
    print(f"[DEBUG] USE_FRESH_ENGINE = {USE_FRESH_ENGINE}")
    
    # Use fresh engine for each speech (more reliable on Windows)
    if USE_FRESH_ENGINE:
        temp_engine = None
        try:
            print("[DEBUG] Creating fresh TTS engine...")
            
            # Create fresh engine with driver specification
            temp_engine = pyttsx3.init('sapi5')  # Explicitly use SAPI5 on Windows
            
            print("[DEBUG] Getting voices...")
            voices = temp_engine.getProperty('voices')
            print(f"[DEBUG] Found {len(voices)} voices")
            
            # Set voice - Use DAVID (male voice) as it's louder and clearer
            voice_set = False
            for voice in voices:
                if 'david' in voice.name.lower():  # Changed from 'zira' to 'david'
                    temp_engine.setProperty('voice', voice.id)
                    print(f"[DEBUG] Using voice: {voice.name}")
                    voice_set = True
                    break
            
            if not voice_set and len(voices) > 0:
                temp_engine.setProperty('voice', voices[0].id)
                print(f"[DEBUG] Using default voice: {voices[0].name}")
            
            # Set properties
            print("[DEBUG] Setting speech properties...")
            temp_engine.setProperty('rate', 150)
            temp_engine.setProperty('volume', 1.0)
            
            # Speak - CRITICAL PART
            print("[DEBUG] Adding text to speech queue...")
            temp_engine.say(text)
            
            print("[DEBUG] Running speech engine (this should produce sound)...")
            temp_engine.runAndWait()
            
            print("[OK] Speech completed successfully!")
            
            # Clean up
            try:
                del temp_engine
            except:
                pass
            
            time.sleep(0.2)  # Increased delay for stability
            return
            
        except Exception as e:
            print(f"[ERROR] Fresh engine failed: {e}")
            import traceback
            traceback.print_exc()
            
            # Cleanup on error
            if temp_engine:
                try:
                    del temp_engine
                except:
                    pass
            
            print("[INFO] Trying fallback method...")
            # Fall through to old method
    
    # Fallback method (original persistent engine)
    print("[DEBUG] Using fallback persistent engine method...")
    
    if not engine:
        print("[DEBUG] Engine not initialized, initializing now...")
        engine = init_engine()
    
    if not engine:
        print(f"[ERROR] TTS not available. Cannot speak: {text}")
        return
    
    try:
        print(f"[DEBUG] Using persistent engine to speak...")
        
        # Method 1: Simple approach
        try:
            print("[DEBUG] Clearing speech queue...")
            engine.stop()
            
            print("[DEBUG] Adding text to queue...")
            engine.say(text)
            
            print("[DEBUG] Running engine...")
            engine.runAndWait()
            
            print("[DEBUG] Clearing queue again...")
            engine.stop()
            
            print("[OK] Speech completed (fallback method)")
            return
            
        except RuntimeError as e:
            print(f"[WARN] RuntimeError in fallback: {e}")
            raise  # Re-raise to trigger reinit
            
    except Exception as e:
        # Last resort: reinitialize and try once more
        print(f"[ERROR] Fallback method failed: {e}")
        print(f"[INFO] Last attempt: Reinitializing engine...")
        
        engine = None
        engine = init_engine()
        
        if engine:
            try:
                engine.say(text)
                engine.runAndWait()
                print("[OK] Speech completed (after reinit)")
            except Exception as e2:
                print(f"[ERROR] All methods failed: {e2}")
                print(f"[TEXT ONLY] {text}")
        else:
            print(f"[ERROR] Cannot initialize TTS engine")
            print(f"[TEXT ONLY] {text}")

def listen():
    r = sr.Recognizer()
    
    # FIX: Adjust recognizer settings for better long-sentence handling
    r.energy_threshold = 300  # Minimum audio energy to consider for recording
    r.dynamic_energy_threshold = True  # Automatically adjust to ambient noise
    r.pause_threshold = 1.5  # INCREASED from 0.8 to 1.5 - allows pauses mid-sentence
    
    try:
        with sr.Microphone() as source:
            print("\n[LISTENING] Speak now...")
            
            # Adjust for ambient noise
            print("[INFO] Adjusting for background noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            # FIX: Increased phrase_time_limit for longer questions
            print("[READY] Speak your command...")
            audio = r.listen(source, timeout=10, phrase_time_limit=30)  # Increased from 15 to 30 seconds
            
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
