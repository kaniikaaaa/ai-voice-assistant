# AI Assistant Zen

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.txt)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

A sophisticated desktop voice assistant powered by ChatGPT and AI, featuring speech recognition, natural language processing, and a modern graphical interface. **Now as smart as ChatGPT with the voice of Alexa!**

## Overview

AI Assistant Zen is a production-ready voice assistant that combines speech recognition, text-to-speech synthesis, and ChatGPT-powered conversational capabilities. The application features secure user authentication, optional wake-word detection, and an intuitive GUI built with modern design principles.

### Key Features

- **🚀 ChatGPT Integration** - Powered by OpenAI GPT for comprehensive knowledge and intelligent responses
- **🎤 Voice Interaction** - Real-time speech recognition with Google Speech API
- **🔊 Alexa-like TTS** - Natural text-to-speech output using pyttsx3
- **✨ Dual AI Support** - Primary: ChatGPT (OpenAI) | Fallback: Google Gemini
- **🔒 Secure Authentication** - User authentication with password hashing
- **🎯 Wake Word Detection** - Optional wake-word detection ("Zen")
- **⚡ Multi-threaded** - Responsive UI with multi-threaded architecture
- **💾 User Management** - SQLite database for user management
- **🎛️ Configurable** - Feature flags for flexible operation modes

## Installation

### Prerequisites

- Python 3.8 or higher
- Microphone and audio output device
- Internet connection (for speech recognition and AI)

### Setup Instructions

**1. Clone the repository**

```bash
git clone https://github.com/kaniikaaaa/ai-voice-assistant.git
cd ai-voice-assistant
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```env
# PRIMARY AI - ChatGPT (OpenAI) - RECOMMENDED FOR BEST RESULTS
OPENAI_API_KEY=your_openai_api_key

# FALLBACK AI - Google Gemini (FREE alternative)
GEMINI_API_KEY=your_gemini_api_key

# Optional: for wake word detection
PORCUPINE_ACCESS_KEY=your_porcupine_key
```

**Get API Keys:**
- **OpenAI (ChatGPT)**: https://platform.openai.com/api-keys - **Recommended for comprehensive knowledge**
- Gemini API: https://makersuite.google.com/app/apikey - **Free alternative**
- Porcupine: https://console.picovoice.ai/ (optional)

**Note:** You need at least ONE AI key (OpenAI or Gemini). OpenAI provides the best ChatGPT-like responses!

**4. Run the application**

```bash
python main.py
```

## Usage

### Getting Started

1. Launch the application
2. Register a new account or login
3. Click "Start Voice Assistant" from the dashboard
4. Begin speaking your commands

### Available Commands

Your assistant can now answer virtually ANY question like ChatGPT!

| Command | Response |
|---------|----------|
| "What time is it?" | Returns current time |
| "What's the date?" | Returns current date |
| "What is 25 times 47?" | Calculates math problems |
| "Tell me a joke" | Responds with a joke |
| "Explain quantum physics" | AI-powered intelligent explanation |
| "Who was Albert Einstein?" | Comprehensive knowledge answers |
| "What is Python programming?" | Technical questions answered |
| "Tell me about World War 2" | Historical information |
| "How do I make pizza?" | Cooking instructions |
| "What's the capital of France?" | General knowledge |
| **ANY question!** | ChatGPT-powered response |
| "Help" | Lists available commands |
| "Exit" / "Quit" | Stops the assistant |

## Configuration

### Feature Flags

Edit `assistant_core.py` to configure operation modes:

```python
# Enable/disable wake word detection
ENABLE_WAKE_WORD = False

# Enable/disable AI responses
USE_AI = True

# Choose AI provider: "openai" (ChatGPT), "gemini", or "both" (fallback)
AI_PROVIDER = "openai"  # Recommended: "openai" for best results
```

### Speech Settings

Modify `speech.py` to adjust voice parameters:

```python
# Speech rate (words per minute)
engine.setProperty('rate', 150)

# Volume level (0.0 to 1.0)
engine.setProperty('volume', 1.0)

# Recognition sensitivity
r.energy_threshold = 300
r.pause_threshold = 0.8
```

## Architecture

### Project Structure

```
ai-voice-assistant/
├── main.py                    # GUI and authentication
├── assistant_core.py          # Core logic and AI integration
├── speech.py                  # Speech recognition and TTS
├── voice assistant_gui.py     # Alternative GUI implementation
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
├── assistant_users.db         # SQLite database
└── *.ppn                      # Wake word model files
```

### Technology Stack

- **Language:** Python 3.8+
- **GUI:** CustomTkinter
- **Speech Recognition:** Google Speech Recognition API
- **Text-to-Speech:** pyttsx3
- **Primary AI:** OpenAI GPT (ChatGPT) - **New!**
- **Fallback AI:** Google Gemini
- **Wake Word Detection:** Porcupine by Picovoice
- **Database:** SQLite3
- **Security:** SHA-256 password hashing

## Troubleshooting

### Microphone Issues

Test your microphone setup:
```bash
python -m speech_recognition
```

Verify microphone permissions are granted in system settings.

### PyAudio Installation (Windows)

If PyAudio fails to install:
```bash
pip install pipwin
pipwin install pyaudio
```

### No AI Responses

- Verify `OPENAI_API_KEY` or `GEMINI_API_KEY` is set in `.env`
- Ensure you've run: `pip install openai`
- Check internet connectivity
- Review console output for error messages
- If OpenAI fails, Gemini will automatically be used as fallback
- See `SETUP_API_KEYS.txt` for detailed instructions

### Text-to-Speech Not Working

- Confirm audio output device is connected
- Check system volume settings
- Try different voice settings in `speech.py`

### Wake Word Not Detecting

- Ensure `PORCUPINE_ACCESS_KEY` is configured in `.env`
- Set `ENABLE_WAKE_WORD = True` in `assistant_core.py`
- Verify `.ppn` model files exist in project directory

## Security

The application implements multiple security measures:

- Password hashing using SHA-256
- No plaintext credential storage
- Email format validation
- Session tracking with timestamps
- Environment-based API key management
- Parameterized database queries

## Development

### Running Without GUI

For testing and debugging:

```bash
python assistant_core.py
```

### Operation Modes

**Wake Word Mode:** Activated by saying "Zen"
**Simple Mode:** Continuously listening without wake word
**ChatGPT Mode:** Intelligent responses using OpenAI GPT (Primary)
**Gemini Mode:** AI responses using Google Gemini (Fallback)
**Basic Mode:** Rule-based responses without AI

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## Author

**Kanika**
- GitHub: [@kaniikaaaa](https://github.com/kaniikaaaa)
- Repository: [ai-voice-assistant](https://github.com/kaniikaaaa/ai-voice-assistant)

## Acknowledgments

- OpenAI for ChatGPT/GPT models and advanced AI capabilities
- Google for Gemini AI and Speech Recognition API
- Picovoice for Porcupine wake word engine
- CustomTkinter for modern UI components
- Open source community for Python libraries
