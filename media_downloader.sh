#!/bin/bash

# 1) Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    # Replace with your package manager command if not using Homebrew
    brew install python3  # For macOS using Homebrew
fi

# 2) Check if venv directory exists, create it if it doesn't
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 3) Activate the venv and install dependencies
echo "Activating virtual environment..."
source venv/bin/activate
echo "Installing dependencies..."
pip install .

# 4) Run the Python script
echo "Running Python script..."
python media_downloader.py

# 5) Deactivate the venv
deactivate
