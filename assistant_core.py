# ai_assistant_zen.py
import requests
import json
import time
import speech_recognition as sr
import os
import struct
import pvporcupine
from dotenv import load_dotenv
import pyaudio
import pyttsx3

# Load environment variables
load_dotenv()
ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")

if not ACCESS_KEY:
    raise ValueError("🚨 PICOVOICE_ACCESS_KEY not found in .env")

# 🎤 Initialize speaker with more detailed error handling
def init_engine():
    try:
        engine = pyttsx3.init()
        if engine:
            voices = engine.getProperty('voices')
            female_voice = None
            for voice in voices:
                if any(k in voice.name.lower() for k in ['female', 'woman', 'girl', 'zira', 'mary', 'helen']):
                    female_voice = voice
                    break

            if female_voice:
                engine.setProperty('voice', female_voice.id)
                print(f"Set voice to female voice: {female_voice.name}")
            else:
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
                    print(f"No female voice found by name, using voice: {voices[1].name}")
                else:
                    print("Only one voice available, using default voice")

            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            engine.runAndWait()
   
            return engine
    except Exception as e:
        print(f"Error initializing text-to-speech engine: {str(e)}")
        return None

# 🧠 More robust speak function with forced sound output
def speak(text):
    global engine
    print(f"🤖 Speaking (attempt): {text}")
    
    success = False
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
            success = True
            print("✅ Speech completed successfully")
        except Exception as e:
            print(f"❌ First speech attempt failed: {str(e)}")
    
    if not success:
        print("🔄 Reinitializing speech engine...")
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
            print("✅ Speech with reinitialized engine completed successfully")
            success = True
        except Exception as e:
            print(f"❌ Second speech attempt failed: {str(e)}")
    
    if not success:
        try:
            import platform
            system = platform.system()
            
            if system == "Darwin":
                import os
                os.system(f'say "{text}"')
                print("✅ Used macOS 'say' command as fallback")
                success = True
            elif system == "Windows":
                try:
                    import win32com.client
                    speaker = win32com.client.Dispatch("SAPI.SpVoice")
                    speaker.Speak(text)
                    print("✅ Used Windows SAPI as fallback")
                    success = True
                except:
                    import subprocess
                    subprocess.call(['powershell', '-command', f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}");'])
                    print("✅ Used PowerShell speech synthesis as fallback")
                    success = True
            elif system == "Linux":
                import os
                try:
                    os.system(f'espeak "{text}"')
                    print("✅ Used Linux 'espeak' as fallback")
                    success = True
                except:
                    try:
                        with open('/tmp/speech.txt', 'w') as f:
                            f.write(text)
                        os.system('festival --tts /tmp/speech.txt')
                        print("✅ Used Linux 'festival' as fallback")
                        success = True
                    except:
                        pass
            
            if not success:
                print("❌ No fallback speech option available for this platform")
        except Exception as e2:
            print(f"❌ Fallback speech method failed: {str(e2)}")
            print("⚠️ Unable to produce speech output")

# 🎙️ Listen Function - converts speech to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.energy_threshold = 300
        r.pause_threshold = 1.6
        r.dynamic_energy_threshold = True
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("🔍 Recognizing speech...")
            try:
                text = r.recognize_google(audio)
                print(f"🎤 You said: {text}")
                return text
            except sr.UnknownValueError:
                print("❓ Sorry, I couldn't understand what you said")
                return ""
            except sr.RequestError as e:
                print(f"🚫 Could not request results from Google Speech Recognition service; {e}")
                return ""
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out. Please try again.")
            return ""
        except Exception as e:
            print(f"🚫 Error in speech recognition: {e}")
            return ""

# 💬 Chat with different AI providers
def chat_with_ai(prompt):
    """Try Groq API first, then fallback options"""
    
    # Option 1: Try Groq API first (best option)
    try:
        print("🚀 Using Groq AI...")
        return chat_with_groq(prompt)
    except Exception as e:
        print(f"❌ Groq API failed: {str(e)}")
    
    # Option 2: Try smaller Ollama models
    small_models = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b", "gemma2:2b"]
    
    for model in small_models:
        try:
            print(f"🔄 Trying Ollama model: {model}")
            url = "http://localhost:11434/api/generate"
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 150
                }
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                response_data = response.json()
                return response_data.get("response", "No response generated")
            else:
                print(f"❌ {model} failed: {response.status_code}")
                continue
        
        except Exception as e:
            print(f"❌ Error with {model}: {str(e)}")
            continue
    
    # Option 3: Try Hugging Face API
    try:
        return chat_with_huggingface(prompt)
    except Exception as e:
        print(f"❌ Hugging Face API failed: {str(e)}")
    
    # Option 4: Fallback to simple responses
    print("🔄 Using fallback responses...")
    return get_fallback_response(prompt)

def chat_with_groq(prompt):
    """Chat with Groq API (requires GROQ_API_KEY in .env)"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Enhanced system prompt for better personality
    system_message = {
        "role": "system", 
        "content": "You are AI Assistant Zen, a helpful and friendly voice assistant. Keep responses conversational, concise (1-3 sentences), and natural for speech. Be warm, helpful, and engaging."
    }
    
    user_message = {
        "role": "user", 
        "content": prompt
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",  # Fast, free model
        "messages": [system_message, user_message],
        "max_tokens": 200,
        "temperature": 0.8,
        "top_p": 0.9
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Groq API error: {response.status_code} - {response.text}")

def chat_with_huggingface(prompt):
    """Chat with Hugging Face API (requires HF_API_KEY in .env)"""
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        raise ValueError("HF_API_KEY not found")
    
    url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    payload = {"inputs": prompt}
    
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "Sorry, I couldn't generate a response.")
        return "Sorry, I couldn't generate a response."
    else:
        raise Exception(f"Hugging Face API error: {response.status_code}")

def get_fallback_response(prompt):
    """Simple rule-based responses as final fallback"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! How can I help you today?"
    elif any(word in prompt_lower for word in ["how", "are", "you"]):
        return "I'm doing well, thank you for asking! How are you?"
    elif any(word in prompt_lower for word in ["what", "your", "name"]):
        return "I'm AI Assistant Zen, your voice assistant!"
    elif any(word in prompt_lower for word in ["weather", "temperature"]):
        return "I don't have access to current weather data, but you can check your local weather app or website."
    elif any(word in prompt_lower for word in ["time", "clock"]):
        return f"I don't have access to the current time, but you can check your system clock."
    elif any(word in prompt_lower for word in ["help", "assist", "will you help"]):
        return "Of course! I'm here to help you. What do you need assistance with?"
    elif any(word in prompt_lower for word in ["thank", "thanks"]):
        return "You're welcome! Is there anything else I can help you with?"
    elif any(word in prompt_lower for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Have a great day!"
    elif any(word in prompt_lower for word in ["good", "fine", "okay", "i am good"]):
        return "That's great to hear! What can I help you with today?"
    else:
        responses = [
            "That's interesting! Can you tell me more?",
            "I understand. What would you like to know?",
            "That's a good question. Let me think about that.",
            "I'm here to help with whatever you need.",
            "Could you provide more details about what you're looking for?"
        ]
        import random
        return random.choice(responses)

# 👂 Wait for wake word "ai assistant zen"
def wait_for_wake_word():
    """Listen for the wake word 'ai assistant zen'"""
    print("🛌 Waiting for 'ai assistant zen' wake word...")

    porcupine = None
    pa = None
    audio_stream = None

    try:
        if not os.path.exists("ai_assistant_zen.ppn"):
            raise FileNotFoundError("Wake word model file 'ai_assistant_zen.ppn' not found. Please create or download it.")
            
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=["ai_assistant_zen.ppn"]
        )

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for 'ai assistant zen'... (Press Ctrl+C to exit)")
        
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)
            if result >= 0:
                print("✅ Wake word 'ai assistant zen' detected!")
                speak("Hi, ai assistant zen is ready to chat!")
                return True

    except KeyboardInterrupt:
        print("\nStopped listening for wake word")
        return False
    except Exception as e:
        print(f"❌ Error in wake word detection: {e}")
        return False
    finally:
        if audio_stream:
            audio_stream.close()
        if pa:
            pa.terminate()
        if porcupine:
            porcupine.delete()

# 🌀 Main loop with voice input and output
def run_babygirl_assistant():
    welcome_message = "Hi user, I'm ai assistant zen, ready to chat!"
    print(welcome_message)
    speak(welcome_message)
    
    print("\n✨ Speak to me and I'll respond with voice ✨")
    print("✨ Say 'exit', 'quit', or 'stop' to end the conversation ✨\n")
    
    while True:
        user_input = listen()
        
        if user_input.lower() in ["exit", "quit", "stop"]:
            goodbye_message = "Okay, bye user!"
            print(goodbye_message)
            speak(goodbye_message)
            break
            
        if not user_input:
            speak("I didn't catch that. Please try again.")
            continue
        
        reply = chat_with_ai(user_input)
        print(f"🤖 ai assistant zen: {reply}")
        speak(reply)

# Initialize the engine at the global level
print("Starting voice assistant system...")
engine = init_engine()

if engine:
    try:
        voices = engine.getProperty('voices')
        print("Available voices:")
        for i, voice in enumerate(voices):
            print(f"Voice {i}: {voice.name}")
        
        female_voice_found = False
        for i, voice in enumerate(voices):
            if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'girl', 'f']):
                engine.setProperty('voice', voice.id)
                print(f"Set voice to female voice: {voice.name}")
                female_voice_found = True
                break
        
        if not female_voice_found and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
            print(f"Set voice to presumed female voice: {voices[1].name}")
        
        engine.say("Voice test for ai assistant zen")
        engine.runAndWait()
    except Exception as e:
        print(f"Error setting voice: {str(e)}")

if __name__ == "__main__":
    try:
        try:
            mics = sr.Microphone.list_microphone_names()
            print(f"🎙️ {len(mics)} microphones detected:")
            for i, mic in enumerate(mics[:5]):
                print(f"  - Mic {i}: {mic}")
            if len(mics) > 5:
                print(f"  - ... and {len(mics)-5} more")
            print("🎙️ Microphone ready for input")
        except Exception as e:
            print(f"⚠️ Warning: Microphone may not be available - {str(e)}")
            print("⚠️ Please ensure you have a working microphone connected")
            print("⚠️ Make sure you've installed PyAudio: pip install pyaudio")
        
        try:
            while True:
                if wait_for_wake_word():
                    run_babygirl_assistant()
                else:
                    print("Wake word detection stopped. Exiting...")
                    break
        except KeyboardInterrupt:
            print("\n👋 Program terminated by user")
        
    except Exception as e:
        print(f"Error in main program: {str(e)}")
    finally:
        if 'engine' in globals() and engine:
            try:
                engine.stop()
            except:
                pass