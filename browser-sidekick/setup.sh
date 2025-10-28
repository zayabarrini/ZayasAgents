#!/bin/bash

echo "🚀 Setting up Browser Sidekick Project..."

# Create virtual environment for backend
echo "📦 Setting up Python backend..."
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -r ../requirements-dev.txt

# Initialize pre-commit hooks
pre-commit install

cd ..

# Setup JavaScript dependencies
echo "📦 Setting up browser extension..."
cd browser-extension
npm install

cd ..

echo "✅ Setup complete!"
echo "🎯 Next steps:"
echo "   1. Add your OpenAI API key to backend/.env"
echo "   2. Run 'cd backend && python server.py' to start the backend"
echo "   3. Load the browser-extension/ folder in Chrome extensions"
echo "   4. Press Ctrl+K on any webpage to activate your sidekick!"