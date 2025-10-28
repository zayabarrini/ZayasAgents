# Install development dependencies
pip install -r requirements-dev.txt

# Initialize pre-commit
pre-commit install

# Run all linters manually
black research_agents/
isort research_agents/
flake8 research_agents/
mypy research_agents/
pylint research_agents/

# Run tests with coverage
pytest --cov=research_agents tests/

# Security audit with bandit
bandit -r research_agents/