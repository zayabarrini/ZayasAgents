#!/bin/bash

echo "Setting up Agentic Engineering Team project..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup pre-commit
pre-commit install

# Create necessary directories
mkdir -p logs test_reports

echo "Setup complete! Activate virtual environment with: source venv/bin/activate"