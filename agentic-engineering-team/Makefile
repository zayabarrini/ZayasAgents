.PHONY: setup test lint format clean docker-run

setup:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt
	pre-commit install

test:
	pytest test_app/ -v

lint:
	black --check .
	flake8 .
	mypy .

format:
	black .
	isort .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache

docker-run:
	docker-compose up --build

dev: format lint test

all: setup dev