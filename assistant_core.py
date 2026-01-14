"""
AI Assistant Core - Voice Assistant Logic
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===== FEATURE FLAGS =====
# Set to True to enable wake word "ZEN", False to disable
ENABLE_WAKE_WORD = False  # Changed to False - wake word disabled by default

# AI Configuration
USE_AI = True  # Set to False to use basic responses only
AI_MODEL = None  # Will be initialized when needed

def run_babygirl_assistant():
    """
    Main voice assistant function
    This function runs the voice assistant loop
    """
    try:
        # Import speech modules
        from speech import speak, listen, init_engine
        
        # Initialize TTS engine (will auto-initialize on first speak() call)
        print("🚀 Starting AI Assistant Zen...")
        init_engine()  # Pre-initialize TTS engine
        
        # Check if wake word is enabled via feature flag
        if not ENABLE_WAKE_WORD:
            print("\n" + "="*50)
            print("📢 WAKE WORD FEATURE DISABLED")
            print("="*50)
            print("Wake word 'ZEN' is currently disabled.")
            print("To enable: Set ENABLE_WAKE_WORD = True in assistant_core.py")
            print("="*50)
            print("\n📢 Running in SIMPLE MODE - no wake word needed")
            print("   Just speak and the assistant will listen!\n")
            run_simple_mode()
            return
        
        # Wake word is enabled - check if Porcupine is available
        try:
            import pvporcupine
            from pvrecorder import PvRecorder
            
            # Get Porcupine access key from environment
            access_key = os.getenv('PORCUPINE_ACCESS_KEY')
            
            if not access_key:
                print("\n" + "="*50)
                print("⚠️  WAKE WORD 'ZEN' - NOT ACTIVATED")
                print("="*50)
                print("To enable wake word 'ZEN':")
                print("1. Get a FREE API key from: https://console.picovoice.ai/")
                print("2. Open the .env file in your project folder")
                print("3. Uncomment and add: PORCUPINE_ACCESS_KEY=your_key_here")
                print("4. Save and restart the assistant")
                print("="*50)
                print("\n📢 Running in SIMPLE MODE - no wake word needed")
                print("   Just speak and the assistant will listen!\n")
                run_simple_mode()
                return
            
            # Run with wake word detection
            run_with_wake_word(access_key)
            
        except ImportError:
            print("⚠️ Porcupine wake word detection not available")
            print("Install with: pip install pvporcupine pvrecorder")
            print("Running in simple listening mode...")
            run_simple_mode()
            
    except Exception as e:
        print(f"❌ Error in assistant: {e}")


def run_simple_mode():
    """
    Simple mode without wake word detection
    Continuously listens and responds
    """
    from speech import speak, listen
    
    print("\n" + "="*50)
    print("🎤 AI ASSISTANT ZEN - SIMPLE MODE")
    print("="*50)
    print("Say something and I'll respond!")
    print("Say 'exit', 'quit', or 'goodbye' to stop.")
    print("="*50 + "\n")
    
    # Test TTS
    print("🧪 Testing text-to-speech...")
    speak("Hello! I'm your AI assistant. How can I help you?")
    
    # Verify microphone
    print("\n✓ If you heard me speak, the voice output is working!")
    print("✓ Make sure your microphone is ready...")
    print("="*50)
    
    while True:
        try:
            print("\n👂 Ready to listen...")
            # Listen for command
            command = listen()
            
            if command:
                print(f"💬 You said: {command}")
                
                # Check for exit commands
                if any(word in command.lower() for word in ['exit', 'quit', 'stop', 'goodbye', 'bye']):
                    print("👋 Exiting...")
                    speak("Goodbye! Have a great day!")
                    break
                
                # Process command
                response = process_command(command)
                print(f"🤖 Assistant: {response}")
                speak(response)
            else:
                print("🔇 No speech detected or recognition failed. Try again...")
            
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def run_with_wake_word(access_key):
    """
    Run assistant with wake word detection (Porcupine)
    """
    import pvporcupine
    from pvrecorder import PvRecorder
    from speech import speak, listen
    
    # Find wake word model file
    wake_word_path = None
    for file in ['ai_assistant_zen.ppn', 'ai-assistant-zen_en_windows_v3_0_0.ppn']:
        if os.path.exists(file):
            wake_word_path = file
            break
    
    if not wake_word_path:
        print("⚠️ Wake word model file not found, falling back to simple mode")
        run_simple_mode()
        return
    
    print("\n" + "="*50)
    print("🎤 AI ASSISTANT ZEN - WAKE WORD MODE ACTIVATED")
    print("="*50)
    print(f"Wake word: 'ZEN'")
    print(f"Model file: {wake_word_path}")
    print("\nSay 'ZEN' to activate the assistant!")
    print("="*50 + "\n")
    
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[wake_word_path]
    )
    
    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    
    try:
        recorder.start()
        print("🎤 Listening for wake word 'ZEN'...")
        print("(Say 'ZEN' to activate)\n")
        
        while True:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("✅ Wake word 'ZEN' detected!")
                speak("Yes? How can I help you?")
                
                # Listen for command
                command = listen()
                
                if command:
                    print(f"💬 You said: {command}")
                    
                    # Check for exit commands
                    if any(word in command.lower() for word in ['exit', 'quit', 'stop', 'goodbye']):
                        print("👋 Exiting...")
                        speak("Goodbye! Have a great day!")
                        break
                    
                    # Process command
                    response = process_command(command)
                    print(f"🤖 Assistant: {response}")
                    speak(response)
                else:
                    print("🔇 No speech detected or recognition failed.")
                
                print("\n🎤 Listening for wake word 'ZEN'...\n")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping assistant...")
    finally:
        recorder.stop()
        recorder.delete()
        porcupine.delete()


def init_ai_model():
    """
    Initialize AI model (Google Gemini)
    """
    global AI_MODEL
    
    if not USE_AI:
        return None
    
    if AI_MODEL is not None:
        return AI_MODEL
    
    try:
        from google import genai
        from google.genai import types
        
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("[WARN] GEMINI_API_KEY not found in .env file")
            print("[WARN] AI responses disabled. Using basic responses only.")
            print("[INFO] Get free API key from: https://makersuite.google.com/app/apikey")
            return None
        
        client = genai.Client(api_key=api_key)
        AI_MODEL = client
        print("[OK] AI Model (Gemini) initialized successfully!")
        return AI_MODEL
        
    except ImportError:
        print("[WARN] google-genai not installed")
        print("[WARN] Install: pip install google-genai")
        return None
    except Exception as e:
        print(f"[WARN] AI initialization failed: {e}")
        return None


def get_ai_response(prompt):
    """
    Get response from AI model
    """
    client = init_ai_model()
    
    if not client:
        return None
    
    try:
        # Create a conversational prompt with system instruction
        system_instruction = """You are a helpful voice assistant named Zen. 
        Keep responses concise (2-3 sentences max) since they will be spoken aloud.
        Be friendly, clear, and helpful. Speak naturally as if talking to a friend."""
        
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
            config={
                'system_instruction': system_instruction,
                'temperature': 0.7,
            }
        )
        
        return response.text
        
    except Exception as e:
        print(f"[WARN] AI response error: {e}")
        return None


def process_command(command):
    """
    Process voice commands and return response using AI
    """
    command_lower = command.lower()
    
    # Quick local commands (no AI needed)
    if any(word in command_lower for word in ['time', 'clock']):
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    if any(word in command_lower for word in ['date', 'today']):
        from datetime import datetime
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"Today is {current_date}"
    
    # Try AI response for everything else
    if USE_AI:
        print("🤖 Thinking...")
        ai_response = get_ai_response(command)
        if ai_response:
            return ai_response
    
    # Fallback to basic responses if AI fails
    if any(word in command_lower for word in ['joke', 'funny']):
        import random
        jokes = [
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
        ]
        return random.choice(jokes)
    
    if 'help' in command_lower:
        return "I can answer questions, tell you the time, date, jokes, and chat with you. What would you like to know?"
    
    # Default response
    return f"I heard you say: {command}. I'm not sure how to respond to that right now."


if __name__ == "__main__":
    run_babygirl_assistant()
8
