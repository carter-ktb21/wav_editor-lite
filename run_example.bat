@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b
)

call venv\Scripts\activate.bat

python wav_editor-lite\main_test.py

pause