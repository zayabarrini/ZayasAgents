#!/bin/bash

set -e

echo "🚀 Setting up Stock Picker Agent Project..."

# Create directory structure
mkdir -p stock_picker_agent/{agents,tasks,tools,data,logs,tests,docs,config,.vscode}
cd stock_picker_agent

# Create Python files
cat > requirements.txt << EOL
crewai
crewai-tools
langchain-openai
yfinance
pandas
numpy
python-dotenv
requests
beautifulsoup4
plotly
tabulate
EOL

cat > requirements-dev.txt << EOL
black
flake8
mypy
pylint
bandit
safety
pre-commit
pytest
pytest-cov
pytest-mock
python-dotenv
EOL

# Create basic config
cat > config.py << EOL
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4"
    MARKET_CAP_THRESHOLD = 1e9
    VOLUME_THRESHOLD = 100000
EOL

# Create .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data
data/
logs/
*.csv
*.json
*.pkl

# OS
.DS_Store
Thumbs.db
EOL

# Create environment template
cat > .env.example << EOL
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_optional
LOG_LEVEL=INFO
EOL

# Create __init__.py files
find . -type d -name "__pycache__" -prune -o -type d -exec touch {}/__init__.py \;

echo "✅ Project structure created!"
echo "📁 Next steps:"
echo "  1. cd stock_picker_agent"
echo "  2. python -m venv venv"
echo "  3. source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "  4. pip install -r requirements.txt -r requirements-dev.txt"
echo "  5. cp .env.example .env"
echo "  6. Add your API keys to .env"
echo "  7. pre-commit install"