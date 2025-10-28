# Makefile
.PHONY: setup lint test clean

setup:
	pip install -r requirements.txt
	pre-commit install
	sqlfluff init

lint:
	sqlfluff lint src/sql/ --config config/sqlfluff.yml
	black src/python/
	flake8 src/python/

lint-fix:
	sqlfluff fix src/sql/ --config config/sqlfluff.yml
	black src/python/

test:
	pytest tests/ -v

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache

run-sql:
	python src/python/sql_runner.py

format:
	black src/python/
	sqlfluff fix src/sql/
	isort src/python/

# Database operations
deploy-models:
	cd src/dbt && dbt run

test-models:
	cd src/dbt && dbt test