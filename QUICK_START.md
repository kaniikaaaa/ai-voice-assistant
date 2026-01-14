# 🚀 Quick Start Guide - AI Assistant Zen

## Your assistant is now upgraded: ChatGPT brain + Alexa voice!

### ⚡ 3-Minute Setup

#### Step 1: Install Dependencies (1 minute)
Double-click: `install_dependencies.bat`

Or run manually:
```bash
pip install -r requirements.txt
pip install openai
```

#### Step 2: Get API Key (1 minute)
**Option A: OpenAI (Best Results - Like ChatGPT)**
1. Go to: https://platform.openai.com/api-keys
2. Sign up/Login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

**Option B: Google Gemini (Free Alternative)**
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy the key

#### Step 3: Create .env File (30 seconds)
Create a file named `.env` in this folder with:

```env
OPENAI_API_KEY=your_key_here
```
OR
```env
GEMINI_API_KEY=your_key_here
```

Replace `your_key_here` with your actual API key!

#### Step 4: Run! (10 seconds)
```bash
python main.py
```

---

## 🎤 How to Use

1. **Register/Login** in the GUI
2. Click **"Start Voice Assistant"**
3. **Start talking!**

### 💬 Example Questions

Try asking:
- "What is the capital of Japan?"
- "Explain how AI works"
- "What is 156 times 23?"
- "Tell me about Albert Einstein"
- "How do I make coffee?"
- "What time is it?"
- **ANY question you'd ask ChatGPT!**

---

## 🔧 Troubleshooting

### "No AI responses"
- ✅ Check your `.env` file exists
- ✅ Verify API key is correct (no extra spaces)
- ✅ Make sure you ran: `pip install openai`

### "Microphone not working"
- ✅ Check microphone permissions in Windows settings
- ✅ Test: Run `python -m speech_recognition`

### "PyAudio won't install"
```bash
pip install pipwin
pipwin install pyaudio
```

---

## 📚 More Help

- **Detailed API setup**: `SETUP_API_KEYS.txt`
- **Full documentation**: `README.md`
- **GitHub Issues**: Report bugs on the repository

---

## 💡 Pro Tips

1. **Best Results**: Use OpenAI (ChatGPT) for most comprehensive knowledge
2. **Free Option**: Use Gemini if you want free tier
3. **Both at once**: Set both keys - OpenAI will be primary, Gemini fallback
4. **Wake Word**: Set `ENABLE_WAKE_WORD = True` in `assistant_core.py` to use "ZEN" wake word

---

**Enjoy your intelligent voice assistant! 🎉**
