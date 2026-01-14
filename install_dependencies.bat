@echo off
echo ============================================
echo AI Assistant Zen - Installing Dependencies
echo ============================================
echo.

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installing main dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Installing OpenAI library (for ChatGPT)...
pip install openai

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo NEXT STEPS:
echo 1. Setup your API keys in .env file
echo 2. See SETUP_API_KEYS.txt for instructions
echo 3. Run: python main.py
echo.
pause
