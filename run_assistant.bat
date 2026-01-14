@echo off
echo ============================================
echo AI Assistant Zen - Starting...
echo ============================================
echo.
echo Make sure:
echo 1. Speakers/headphones are connected
echo 2. Microphone is connected
echo 3. Volume is not muted
echo.
echo Press any key to start...
pause
echo.
echo Starting AI Assistant...
echo.

cd /d "%~dp0"
.venv\Scripts\python.exe assistant_core.py

pause
