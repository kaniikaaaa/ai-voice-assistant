# AI Assistant Zen - Feature Flags

## ✅ Changes Made

### 1. Wake Word Feature Flag (Porcupine)
**Location:** `assistant_core.py` - Line 13

```python
# Set to True to enable wake word "ZEN", False to disable
ENABLE_WAKE_WORD = False  # Currently disabled
```

**How to use:**
- **Disabled (Default):** Assistant continuously listens without wake word
- **Enabled:** Assistant waits for wake word "ZEN" before listening

**To Enable:**
1. Open `assistant_core.py`
2. Change line 13: `ENABLE_WAKE_WORD = False` → `ENABLE_WAKE_WORD = True`
3. Get Porcupine API key from https://console.picovoice.ai/
4. Add key to `.env` file: `PORCUPINE_ACCESS_KEY=your_key`
5. Restart assistant

---

### 2. Response Mode - Text + Voice ✅

**Already Implemented!**

The assistant automatically responds in **BOTH** ways:

1. **📝 Text Output** - Displayed in console
   ```
   🤖 Assistant: The current time is 3:45 PM
   ```

2. **🔊 Voice Output** - Spoken using text-to-speech
   - Text is automatically converted to speech
   - Uses pyttsx3 engine

**Code Reference:**
```python
# Line 111 & 186 in assistant_core.py
print(f"🤖 Assistant: {response}")  # Text output
speak(response)                      # Voice output
```

---

## 🚀 Quick Start

### Run Assistant (Current Settings):
```bash
.venv\Scripts\python.exe assistant_core.py
```

**Current Configuration:**
- ❌ Wake word: Disabled
- ✅ Continuous listening: Enabled
- ✅ Text response: Enabled
- ✅ Voice response: Enabled

### What Happens:
1. Assistant starts listening immediately (no wake word needed)
2. You speak your command
3. Assistant shows response in text: `🤖 Assistant: [response]`
4. Assistant speaks response: Audio output
5. Assistant continues listening

---

## 🎯 Test Commands

Try these:
- "What time is it?"
- "What's the date today?"
- "Tell me a joke"
- "Help"
- "Exit" / "Goodbye" (to quit)

---

## 📋 Summary

| Feature | Status | Location |
|---------|--------|----------|
| Wake Word "ZEN" | ❌ Disabled | `assistant_core.py` line 13 |
| Continuous Listening | ✅ Enabled | Default when wake word is off |
| Text Response | ✅ Enabled | Line 111, 186 |
| Voice Response | ✅ Enabled | Line 112, 187 |
| Regex Email Validation | ✅ Enabled | `main.py` |

---

## 🔧 Customize

### Disable Voice (text only):
Comment out `speak(response)` on lines 112 and 187

### Enable Wake Word:
Set `ENABLE_WAKE_WORD = True` in `assistant_core.py`

### Change Voice Settings:
Edit `speech.py` - adjust rate, volume, voice gender
