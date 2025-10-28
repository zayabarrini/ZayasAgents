#!/bin/bash

# Agentic Research Project Setup Script

echo "🚀 Setting up Agentic Research Project..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install pre-commit hooks
echo "🔨 Installing pre-commit hooks..."
pre-commit install

# Run initial formatting
echo "✨ Running initial code formatting..."
black src/ tests/
isort src/ tests/

echo "✅ Setup complete! Activate virtual environment with: source venv/bin/activate"