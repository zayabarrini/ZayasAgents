.PHONY: install setup test lint format clean run

install:
	pip install -r requirements.txt -r requirements-dev.txt

setup:
	pre-commit install

test:
	pytest -v

lint:
	black .
	flake8 .
	mypy .

format:
	black .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache .pytest_cache

run:
	python main.py

quick:
	python quick_start.py

security:
	bandit -r .
	safety check

all: lint test security