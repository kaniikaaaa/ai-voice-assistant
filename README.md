# Zen

Voice-activated desktop assistant with a wake word, dual-LLM fallback, and a native Tk UI. Say "Zen", ask a question, get a spoken reply; OpenAI is the primary brain, Gemini is the automatic fallback if OpenAI rate-limits or fails.

## Stack

Python · CustomTkinter · Picovoice Porcupine (wake word) · SpeechRecognition · pyttsx3 · OpenAI · Google Gemini · SQLite

## What's interesting here

- **Hot-word gated, always listening.** Porcupine runs in a background thread waiting for "Zen"; only after the wake-word fires does the mic buffer go to ASR. Privacy win and CPU win.
- **Dual-LLM fallback chain.** Primary call is OpenAI chat completions; on any exception (timeout, rate limit, 5xx) the request is transparently re-routed to Gemini. Fallback is explicit, not hidden; the UI logs which model answered.
- **Session memory in SQLite.** Conversation turns are persisted locally so context survives across launches. No cloud session store, no signup.

## Run locally

```bash
git clone https://github.com/kaniikaaaa/ai-voice-assistant.git
cd ai-voice-assistant

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# macOS/Linux may also need PortAudio:
#   macOS:  brew install portaudio
#   Ubuntu: sudo apt install portaudio19-dev

cp .env.example .env
# Fill: OPENAI_API_KEY, GOOGLE_API_KEY, PICOVOICE_ACCESS_KEY

python main.py
```

## Files

```
main.py             Tk UI, event loop
assistant_core.py   LLM routing, fallback chain, memory
speech.py           Porcupine wake word, ASR, TTS
```

## Keyboard shortcuts

- `Enter`: send typed message
- `Space` (hold): push-to-talk override
- `Esc`: close

## License

MIT
