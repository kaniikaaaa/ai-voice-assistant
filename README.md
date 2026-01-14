AI Assistant Zen

AI Assistant Zen is a desktop-based voice assistant that integrates speech recognition, text-to-speech, and generative AI to enable natural, real-time interaction through voice commands. The system is designed with a modular architecture, secure authentication, and a responsive graphical interface.

Features

Real-time speech recognition using microphone input

Text-to-speech output with configurable voice and rate

AI-powered responses using Google Gemini for conversational intelligence

Optional wake-word detection using Porcupine

Fast local command handling for time, date, and utility queries

Secure user authentication with password hashing

SQLite database for user management and session tracking

Multi-threaded execution to prevent GUI blocking

Environment-based configuration using .env files

Feature flags to enable or disable AI and wake-word functionality

Tech Stack

Python

CustomTkinter (GUI)

SpeechRecognition

pyttsx3 (TTS)

Google Gemini API

SQLite

Porcupine (Wake-word detection)

threading, dotenv, hashlib

Project Structure
.
├── assistant_core.py       # Core assistant logic and AI integration
├── speech.py               # Speech recognition and text-to-speech
├── main.py                 # GUI with authentication and dashboard
├── voice_assistant_gui.py  # Alternative GUI implementation
├── assistant_users.db      # SQLite database
├── .env                    # API keys and environment variables

Setup Instructions

Clone the repository

git clone <repository-url>
cd <project-folder>


Install dependencies

pip install -r requirements.txt


Create a .env file

GEMINI_API_KEY=your_gemini_api_key
PORCUPINE_ACCESS_KEY=your_porcupine_api_key   # Optional


Run the application

python main.py

Configuration

Inside assistant_core.py:

ENABLE_WAKE_WORD = False
USE_AI = True


Set ENABLE_WAKE_WORD = True to activate wake-word detection

Set USE_AI = False to run in rule-based mode without Gemini

How It Works

User logs in or registers through the GUI

The assistant runs in a background thread

Speech is captured and converted to text

Commands are routed either to:

Local handlers (time, date, jokes)

Gemini API for intelligent responses

The response is converted to speech and played back

Security

Passwords are hashed using SHA-256

No plaintext credentials are stored

SQLite ensures lightweight and local data persistence

Use Case

This project demonstrates the design of a production-style AI assistant combining:

AI model integration

Voice processing

GUI development

Database-backed authentication

Scalable and maintainable software architecture

It reflects strong capability in building end-to-end intelligent systems rather than isolated features.
