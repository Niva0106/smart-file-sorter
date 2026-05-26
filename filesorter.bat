@echo off
cd /d %~dp0

echo Checking virtual environment...

if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Starting application...
python main.py

pause