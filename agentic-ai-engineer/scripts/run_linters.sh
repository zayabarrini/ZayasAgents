#!/bin/bash

# Comprehensive Linting and Quality Check Script

echo "🔍 Running code quality checks..."

echo "1. Running Black..."
python -m black --check .

echo "2. Running isort..."
python -m isort --check-only .

echo "3. Running flake8..."
python -m flake8 .

echo "4. Running mypy..."
python -m mypy .

echo "5. Running pylint..."
python -m pylint agent_creator.py agent_manager.py advanced_agent_creator.py utils/ config/

echo "6. Running bandit (security)..."
python -m bandit -r .

echo "7. Running pytest..."
python -m pytest tests/ -v

echo "✅ All checks completed!"