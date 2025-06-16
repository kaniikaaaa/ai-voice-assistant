# 📁 core/speech.py
import pyttsx3
import speech_recognition as sr

engine = None

def init_engine():
    global engine
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'girl', 'zira']):
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        return engine
    except Exception as e:
        print(f"TTS init error: {e}")
        return None

def speak(text):
    global engine
    if not engine:
        engine = init_engine()
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            return r.recognize_google(audio)
        except:
            return ""
