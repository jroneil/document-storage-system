#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment based on OS
if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  source venv/Scripts/activate
else
  source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt
pip install "uvicorn[standard]"

echo "Virtual environment created and activated. Dependencies installed."