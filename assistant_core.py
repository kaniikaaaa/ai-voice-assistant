"""
AI Assistant Core - Voice Assistant Logic
Enhanced with ChatGPT (OpenAI) + Gemini Support
"""
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===== FEATURE FLAGS =====
# Set to True to enable wake word "ZEN", False to disable
ENABLE_WAKE_WORD = False  # Changed to False - wake word disabled by default

# AI Configuration
USE_AI = True  # Set to False to use basic responses only
AI_PROVIDER = "openai"  # Options: "openai" (ChatGPT), "gemini", "both"
OPENAI_CLIENT = None  # OpenAI client
GEMINI_CLIENT = None  # Gemini client

def run_babygirl_assistant():
    """
    Main voice assistant function
    This function runs the voice assistant loop
    """
    try:
        # Import speech modules
        from speech import speak, listen, init_engine
        
        # Initialize TTS engine (will auto-initialize on first speak() call)
        print("[START] Starting AI Assistant Zen...")
        init_engine()  # Pre-initialize TTS engine
        
        # Check if wake word is enabled via feature flag
        if not ENABLE_WAKE_WORD:
            print("\n" + "="*50)
            print("[INFO] WAKE WORD FEATURE DISABLED")
            print("="*50)
            print("Wake word 'ZEN' is currently disabled.")
            print("To enable: Set ENABLE_WAKE_WORD = True in assistant_core.py")
            print("="*50)
            print("\n[MODE] Running in SIMPLE MODE - no wake word needed")
            print("       Just speak and the assistant will listen!\n")
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
                print("[WARN] WAKE WORD 'ZEN' - NOT ACTIVATED")
                print("="*50)
                print("To enable wake word 'ZEN':")
                print("1. Get a FREE API key from: https://console.picovoice.ai/")
                print("2. Open the .env file in your project folder")
                print("3. Uncomment and add: PORCUPINE_ACCESS_KEY=your_key_here")
                print("4. Save and restart the assistant")
                print("="*50)
                print("\n[MODE] Running in SIMPLE MODE - no wake word needed")
                print("       Just speak and the assistant will listen!\n")
                run_simple_mode()
                return
            
            # Run with wake word detection
            run_with_wake_word(access_key)
            
        except ImportError:
            print("[WARN] Porcupine wake word detection not available")
            print("Install with: pip install pvporcupine pvrecorder")
            print("Running in simple listening mode...")
            run_simple_mode()
            
    except Exception as e:
        print(f"[ERROR] Error in assistant: {e}")


def run_simple_mode():
    """
    Simple mode without wake word detection
    Continuously listens and responds
    """
    from speech import speak, listen
    
    print("\n" + "="*50)
    print("[MODE] AI ASSISTANT ZEN - SIMPLE MODE")
    print("="*50)
    print("Say something and I'll respond!")
    print("Say 'exit', 'quit', or 'goodbye' to stop.")
    print("="*50 + "\n")
    
    # Test TTS
    print("[TEST] Testing text-to-speech...")
    print("[INFO] You should hear me speak now...")
    speak("Hello! I'm your AI assistant powered by ChatGPT. How can I help you?")
    
    # Verify with user
    print("\n" + "="*50)
    print("[IMPORTANT] Did you hear me speak? (Y/N)")
    print("="*50)
    print("[INFO] If NO:")
    print("  1. Check speakers/headphones are connected")
    print("  2. Check Windows volume is not muted")  
    print("  3. Press Ctrl+C to exit and run: python test_voice.py")
    print("="*50)
    print("\n[OK] Make sure your microphone is ready...")
    print("[OK] Starting listening mode...")
    print("="*50)
    
    while True:
        try:
            print("\n[READY] Listening...")
            # Listen for command
            command = listen()
            
            if command:
                print(f"[USER] You said: {command}")
                
                # Check for exit commands
                if any(word in command.lower() for word in ['exit', 'quit', 'stop', 'goodbye', 'bye']):
                    print("[EXIT] Exiting...")
                    speak("Goodbye! Have a great day!")
                    break
                
                # Process command
                response = process_command(command)
                print(f"[ASSISTANT] {response}")
                speak(response)
            else:
                print("[WARN] No speech detected or recognition failed. Try again...")
            
        except KeyboardInterrupt:
            print("\n[EXIT] Exiting...")
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"[ERROR] {e}")


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
        print("[WARN] Wake word model file not found, falling back to simple mode")
        run_simple_mode()
        return
    
    print("\n" + "="*50)
    print("[MODE] AI ASSISTANT ZEN - WAKE WORD MODE ACTIVATED")
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
        print("[LISTENING] Listening for wake word 'ZEN'...")
        print("(Say 'ZEN' to activate)\n")
        
        while True:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("[DETECTED] Wake word 'ZEN' detected!")
                speak("Yes? How can I help you?")
                
                # Listen for command
                command = listen()
                
                if command:
                    print(f"[USER] You said: {command}")
                    
                    # Check for exit commands
                    if any(word in command.lower() for word in ['exit', 'quit', 'stop', 'goodbye']):
                        print("[EXIT] Exiting...")
                        speak("Goodbye! Have a great day!")
                        break
                    
                    # Process command
                    response = process_command(command)
                    print(f"[ASSISTANT] {response}")
                    speak(response)
                else:
                    print("[WARN] No speech detected or recognition failed.")
                
                print("\n[LISTENING] Listening for wake word 'ZEN'...\n")
                
    except KeyboardInterrupt:
        print("\n[STOP] Stopping assistant...")
    finally:
        recorder.stop()
        recorder.delete()
        porcupine.delete()


def init_openai():
    """
    Initialize OpenAI GPT (ChatGPT) - PRIMARY AI
    """
    global OPENAI_CLIENT
    
    if OPENAI_CLIENT is not None:
        return OPENAI_CLIENT
    
    try:
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("[WARN] OPENAI_API_KEY not found in .env file")
            print("[INFO] Get API key from: https://platform.openai.com/api-keys")
            return None
        
        OPENAI_CLIENT = OpenAI(api_key=api_key)
        print("[OK] ChatGPT (OpenAI) initialized successfully! 🚀")
        return OPENAI_CLIENT
        
    except ImportError:
        print("[WARN] openai library not installed")
        print("[WARN] Install: pip install openai")
        return None
    except Exception as e:
        print(f"[WARN] OpenAI initialization failed: {e}")
        return None


def init_gemini():
    """
    Initialize Google Gemini AI - FALLBACK AI
    """
    global GEMINI_CLIENT
    
    if GEMINI_CLIENT is not None:
        return GEMINI_CLIENT
    
    try:
        from google import genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("[WARN] GEMINI_API_KEY not found in .env file")
            print("[INFO] Get free API key from: https://makersuite.google.com/app/apikey")
            return None
        
        GEMINI_CLIENT = genai.Client(api_key=api_key)
        print("[OK] Gemini AI initialized successfully! ✨")
        return GEMINI_CLIENT
        
    except ImportError:
        print("[WARN] google-genai not installed")
        print("[WARN] Install: pip install google-genai")
        return None
    except Exception as e:
        print(f"[WARN] Gemini initialization failed: {e}")
        return None


def get_ai_response(prompt):
    """
    Get intelligent response from AI (ChatGPT primary, Gemini fallback)
    """
    if not USE_AI:
        return None
    
    system_prompt = """You are Zen, an intelligent voice assistant like Alexa but powered by advanced AI.
You have comprehensive knowledge like ChatGPT - you can answer questions about science, history, math, 
programming, general knowledge, current events, and any topic.

Keep responses:
- Concise (2-4 sentences) since they'll be spoken aloud
- Natural and conversational
- Accurate and helpful
- Friendly but professional

If you don't know something, be honest but helpful."""
    
    # Try OpenAI (ChatGPT) first - Most powerful option
    if AI_PROVIDER in ["openai", "both"]:
        try:
            client = init_openai()
            if client:
                print("[AI] Using ChatGPT...")
                print(f"[AI] Sending question: {prompt[:50]}...")
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Fast and cost-effective
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=150,
                    timeout=30  # 30 second timeout
                )
                answer = response.choices[0].message.content.strip()
                print(f"[AI] ✓ Got ChatGPT Response!")
                print(f"[AI] Response: {answer}")
                return answer
        except Exception as e:
            print(f"[ERROR] ChatGPT error: {e}")
            import traceback
            traceback.print_exc()
            if AI_PROVIDER == "openai":
                print("[INFO] Trying Gemini as fallback...")
    
    # Try Gemini as fallback or if selected
    if AI_PROVIDER in ["gemini", "both"] or OPENAI_CLIENT is None:
        try:
            client = init_gemini()
            if client:
                print("[AI] Using Gemini AI...")
                response = client.models.generate_content(
                    model='gemini-2.0-flash-exp',
                    contents=prompt,
                    config={
                        'system_instruction': system_prompt,
                        'temperature': 0.7,
                    }
                )
                answer = response.text.strip()
                print(f"[AI] Gemini Response: {answer[:50]}...")
                return answer
        except Exception as e:
            print(f"[WARN] Gemini error: {e}")
    
    print("[ERROR] No AI service available!")
    return None


def process_command(command):
    """
    Process voice commands and return intelligent AI-powered responses
    Now handles ALL questions like ChatGPT!
    """
    command_lower = command.lower()
    
    print(f"[PROCESSING] Command: {command}")
    
    # Quick local responses (faster than AI)
    
    # Math calculation - Quick pattern matching for simple math
    if any(word in command_lower for word in ['plus', 'minus', 'times', 'multiply', 'divide', 'into']):
        # Try to handle basic math locally (faster)
        try:
            math_patterns = [
                (r'(\d+\.?\d*)\s*(?:plus|\+)\s*(\d+\.?\d*)', lambda a, b: float(a) + float(b), 'plus'),
                (r'(\d+\.?\d*)\s*(?:minus|-)\s*(\d+\.?\d*)', lambda a, b: float(a) - float(b), 'minus'),
                (r'(\d+\.?\d*)\s*(?:times|multiply|multiplied by|\*|into)\s*(\d+\.?\d*)', lambda a, b: float(a) * float(b), 'times'),
                (r'(\d+\.?\d*)\s*(?:divide|divided by|/)\s*(\d+\.?\d*)', lambda a, b: float(a) / float(b) if float(b) != 0 else None, 'divided by'),
            ]
            
            for pattern, operation, op_name in math_patterns:
                match = re.search(pattern, command_lower)
                if match:
                    num1, num2 = match.groups()
                    result = operation(num1, num2)
                    if result is not None:
                        result_str = str(int(result)) if result == int(result) else str(result)
                        return f"{num1} {op_name} {num2} equals {result_str}"
                    else:
                        return "I cannot divide by zero"
        except Exception as e:
            print(f"[WARN] Math calculation failed: {e}")
            # Fall through to AI
    
    # Time check (use more specific matching)
    if re.search(r'\b(what|current|what\'s|whats)\s+(time|clock)\b', command_lower) or 'time is it' in command_lower:
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    # Date check
    if any(phrase in command_lower for phrase in ['what date', "today's date", 'what is today', 'current date']):
        from datetime import datetime
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"Today is {current_date}"
    
    # Try AI response for EVERYTHING else - This is where the magic happens!
    if USE_AI:
        print("[AI] 🤔 Thinking with ChatGPT/AI brain...")
        ai_response = get_ai_response(command)
        if ai_response:
            return ai_response
        else:
            print("[WARN] AI service unavailable. Check your API keys in .env file!")
    
    # Fallback to basic responses only if AI completely fails
    print("[INFO] Using fallback responses (AI not available)")
    
    if any(word in command_lower for word in ['joke', 'funny']):
        import random
        jokes = [
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
        ]
        return random.choice(jokes)
    
    if 'help' in command_lower:
        return "I can answer ANY question like ChatGPT! Ask me about science, history, math, programming, or anything. I can also tell you the time and date. What would you like to know?"
    
    # Default response when AI is not available
    return "I need an AI API key to answer that. Please check the SETUP_API_KEYS.txt file to configure OpenAI or Gemini."


if __name__ == "__main__":
    run_babygirl_assistant()
8
