# 🎤 AI Assistant Zen

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**A sophisticated desktop voice assistant powered by AI, featuring speech recognition, natural language processing, and a modern GUI.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#️-configuration)

</div>

---

## 📋 Overview

**AI Assistant Zen** is a production-ready voice assistant application that combines cutting-edge speech recognition, text-to-speech synthesis, and AI-powered conversational capabilities. Built with a modular architecture, it features secure user authentication, optional wake-word detection, and an intuitive graphical interface.

### 🎯 Key Highlights

- 🎙️ **Real-time Speech Recognition** - Continuous voice input processing
- 🔊 **Natural Text-to-Speech** - Human-like voice responses
- 🤖 **AI-Powered Intelligence** - Google Gemini integration for smart conversations
- 🔐 **Secure Authentication** - Password hashing and SQLite database
- 🎨 **Modern GUI** - Beautiful CustomTkinter interface
- ⚡ **Multi-threaded** - Non-blocking UI with background processing
- 🎯 **Wake Word Detection** - Optional "Zen" activation (Porcupine)
- 🔧 **Feature Flags** - Easy configuration for different modes

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Voice Recognition** | Google Speech Recognition with ambient noise adjustment |
| **AI Responses** | Powered by Google Gemini for intelligent, context-aware replies |
| **Text-to-Speech** | Natural voice output using pyttsx3 |
| **Wake Word** | Optional activation using custom "Zen" wake word |
| **User Management** | Registration, login, and session tracking |
| **Fast Commands** | Instant local responses for time, date, and common queries |
| **Secure Storage** | SHA-256 password hashing with SQLite database |

### Modes of Operation

1. **Wake Word Mode** - Say "Zen" to activate the assistant
2. **Simple Mode** - Always listening, no wake word required
3. **AI Mode** - Intelligent responses using Google Gemini
4. **Basic Mode** - Rule-based responses without AI

---

## 🚀 Demo

### Voice Interaction Flow

```
👤 User: "Hey Zen, what's the weather like today?"
🤖 Assistant: "I can help you with that! Currently, I can provide time, date, and answer questions. For real-time weather, I'd need additional API integration."

👤 User: "Tell me a joke"
🤖 Assistant: "Why do programmers prefer dark mode? Because light attracts bugs!"

👤 User: "What time is it?"
🤖 Assistant: "The current time is 3:45 PM"
```

---

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **Microphone** and **Speakers**
- **Internet Connection** (for speech recognition and AI)
- **Windows/Linux/macOS** (tested on Windows)

### Step 1: Clone the Repository

```bash
git clone https://github.com/kaniikaaaa/ai-voice-assistant.git
cd ai-voice-assistant
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
```
customtkinter>=5.2.0
python-dotenv>=1.0.0
pyttsx3>=2.90
SpeechRecognition>=3.10.0
pyaudio>=0.2.13
pvporcupine>=3.0.0
pvrecorder>=1.2.0
google-genai>=1.0.0
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Required for AI responses
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Only needed if using wake word detection
PORCUPINE_ACCESS_KEY=your_porcupine_access_key_here
```

**Get API Keys:**
- **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey) (Free tier available)
- **Porcupine**: [Picovoice Console](https://console.picovoice.ai/) (Optional, for wake word)

### Step 4: Run the Application

```bash
python main.py
```

---

## 🎮 Usage

### First Time Setup

1. **Launch** the application: `python main.py`
2. **Register** a new account with email and password
3. **Login** with your credentials
4. **Start** the voice assistant from the dashboard

### Voice Commands

| Command | Response |
|---------|----------|
| `"What time is it?"` | Current time |
| `"What's the date?"` | Current date |
| `"Tell me a joke"` | Random programming joke |
| `"Help"` | Available commands |
| `"Exit"` / `"Quit"` | Stop assistant |
| Any question | AI-powered response |

### GUI Features

- **Authentication Screen** - Secure login/registration
- **User Dashboard** - View profile and statistics
- **Assistant Control** - Start/stop voice assistant
- **Status Indicators** - Real-time feedback

---

## ⚙️ Configuration

### Feature Flags (in `assistant_core.py`)

```python
# Enable/Disable wake word detection
ENABLE_WAKE_WORD = False  # Set to True to enable "Zen" wake word

# Enable/Disable AI responses
USE_AI = True  # Set to False for basic rule-based responses only
```

### Speech Settings (in `speech.py`)

```python
# Text-to-Speech Configuration
engine.setProperty('rate', 150)    # Speech speed (default: 150)
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# Speech Recognition Sensitivity
r.energy_threshold = 300           # Audio energy threshold
r.pause_threshold = 0.8            # Silence duration (seconds)
```

---

## 🏗️ Project Structure

```
ai-voice-assistant/
│
├── main.py                    # GUI application with authentication
├── assistant_core.py          # Core voice assistant logic and AI
├── speech.py                  # Speech recognition and TTS
├── voice assistant_gui.py     # Alternative GUI implementation
│
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in repo)
├── assistant_users.db         # SQLite database (auto-created)
│
├── ai_assistant_zen.ppn       # Wake word model files
├── LICENSE.txt                # Project license
└── README.md                  # This file
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **Microphone Not Working**
```bash
# Test microphone
python -m speech_recognition
```
- Ensure microphone permissions are granted
- Check default input device in system settings

#### 2. **PyAudio Installation Error (Windows)**
```bash
# Install pre-built wheel
pip install pipwin
pipwin install pyaudio
```

#### 3. **No AI Responses**
- Verify `GEMINI_API_KEY` in `.env` file
- Check internet connection
- View console for error messages

#### 4. **TTS Not Speaking**
- Ensure speakers/headphones are connected
- Check system volume settings
- Try different voice in `speech.py`

#### 5. **Wake Word Not Detecting**
- Verify `PORCUPINE_ACCESS_KEY` in `.env`
- Check `ENABLE_WAKE_WORD = True` in `assistant_core.py`
- Ensure `.ppn` model files exist

---

## 🧪 Running Without GUI

For command-line testing:

```bash
python assistant_core.py
```

This runs the assistant directly without the GUI, useful for debugging.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **GUI Framework** | CustomTkinter |
| **Speech Recognition** | Google Speech Recognition API |
| **Text-to-Speech** | pyttsx3 |
| **AI Model** | Google Gemini (gemini-flash-latest) |
| **Wake Word** | Porcupine by Picovoice |
| **Database** | SQLite3 |
| **Authentication** | SHA-256 hashing |
| **Environment** | python-dotenv |

---

## 🔐 Security Features

- ✅ **Password Hashing** - SHA-256 with no plaintext storage
- ✅ **Email Validation** - Regex-based format checking
- ✅ **Session Management** - Login tracking and timestamps
- ✅ **Environment Variables** - Secure API key storage
- ✅ **Database Security** - SQLite with parameterized queries

---

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Conversation history with context
- [ ] Integration with smart home devices
- [ ] Weather API integration
- [ ] Calendar and reminder functionality
- [ ] Voice biometrics for authentication
- [ ] Cloud synchronization
- [ ] Mobile companion app

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

---

## 👨‍💻 Author

**Kanika**

- GitHub: [@kaniikaaaa](https://github.com/kaniikaaaa)
- Project: [ai-voice-assistant](https://github.com/kaniikaaaa/ai-voice-assistant)

---

## 🙏 Acknowledgments

- **Google** - Gemini AI and Speech Recognition API
- **Picovoice** - Porcupine wake word engine
- **CustomTkinter** - Modern UI framework
- **Open Source Community** - For amazing Python libraries

---

## 📞 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an [Issue](https://github.com/kaniikaaaa/ai-voice-assistant/issues)
3. Review existing issues and discussions

---

<div align="center">

**⭐ If you find this project helpful, please give it a star!**

Made with ❤️ by Kanika

</div>
