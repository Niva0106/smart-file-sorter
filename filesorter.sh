#!/bin/bash

cd "$(dirname "$0")"

echo "Checking virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting application..."
python3 main.py