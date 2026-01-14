@echo off
echo ============================================
echo AI Assistant Zen - API Key Setup
echo ============================================
echo.
echo STEP 1: Get your OpenAI API key
echo --------------------------------
echo 1. Visit: https://platform.openai.com/api-keys
echo 2. Sign up or login
echo 3. Click "Create new secret key"
echo 4. Copy the key (starts with sk-)
echo.
echo STEP 2: Enter your API key below
echo ---------------------------------
echo.
set /p apikey="Paste your OpenAI API key here: "
echo.
echo Creating .env file...
(
echo # AI Assistant Configuration
echo OPENAI_API_KEY=%apikey%
) > .env
echo.
echo ============================================
echo SUCCESS! .env file created!
echo ============================================
echo.
echo You can now run: python main.py
echo.
pause
