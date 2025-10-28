#!/bin/bash

echo "🚀 Setting up Trading Floor Development Environment..."

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -e .[dev]

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

# Create environment file
cp .env.example .env

echo "✅ Development environment setup complete!"
echo "📝 Update .env file with your API keys and configuration"
echo "🚀 To start developing: source venv/bin/activate"