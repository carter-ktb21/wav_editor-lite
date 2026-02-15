@echo off
cd /d "%~dp0"

echo Creating venv with Python 3.12...

py -3.12 --version >nul 2>nul
if errorlevel 1 (
    echo.
    echo Python 3.12 not found.
    echo Please install it from python.org first.
    echo.
    pause
    exit /b
)

echo Creating virtual environment...
py -3.12 -m venv venv

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete
echo Now run run.bat

pause