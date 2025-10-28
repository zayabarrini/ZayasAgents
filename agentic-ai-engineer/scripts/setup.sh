#!/bin/bash

# Agent Creator Project Setup Script

echo "🚀 Setting up Agentic AI Engineer Project..."

# Create virtual environment
python3.9 -m venv .venv
echo "✅ Virtual environment created"

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Create necessary directories
mkdir -p agents logs

# Set up environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys"
fi

# Run initial tests
echo "🧪 Running initial tests..."
python -m pytest tests/ -v

echo "🎉 Setup complete! Activate virtual environment with: source .venv/bin/activate"