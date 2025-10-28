#!/bin/bash

# Setup script for Career Digital Twin

echo "Setting up Career Digital Twin project..."

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Setup frontend
cd frontend
npm install

echo "Setup complete!"
echo "To start developing:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Start backend: python backend/server.py"
echo "3. Open http://localhost:5000 in your browser"