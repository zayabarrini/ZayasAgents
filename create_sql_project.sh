#!/bin/bash

# Create the complete project structure
mkdir -p agentic-ai-sql-project/{src/{sql,python,dbt/{models/{staging,marts/{core,analytics}},tableau},data/{raw,processed,models},docs,tests,sql_scripts,config,notebooks,dashboards}

# Create specific SQL and configuration files
touch agentic-ai-sql-project/.gitignore
touch agentic-ai-sql-project/README.md
touch agentic-ai-sql-project/requirements.txt
touch agentic-ai-sql-project/dbt_project.yml

# SQL files
touch agentic-ai-sql-project/src/sql/data_modeling.sql
touch agentic-ai-sql-project/src/sql/ab_test_analysis.sql
touch agentic-ai-sql-project/src/sql/data_quality_monitoring.sql
touch agentic-ai-sql-project/src/sql/tableau_optimized_views.sql
touch agentic-ai-sql-project/src/sql/session_analysis.sql
touch agentic-ai-sql-project/src/sql/user_funnel.sql
touch agentic-ai-sql-project/src/sql/cohort_analysis.sql
touch agentic-ai-sql-project/src/sql/instrumentation_checks.sql

# Python files
touch agentic-ai-sql-project/src/python/ab_test_analyzer.py
touch agentic-ai-sql-project/src/python/data_quality.py
touch agentic-ai-sql-project/src/python/sql_runner.py
touch agentic-ai-sql-project/src/python/tableau_integration.py
touch agentic-ai-sql-project/src/python/utils.py

# DBT models
touch agentic-ai-sql-project/src/dbt/schema.yml
touch agentic-ai-sql-project/src/dbt/sources.yml
touch agentic-ai-sql-project/src/dbt/models/staging/stg_events.sql
touch agentic-ai-sql-project/src/dbt/models/staging/stg_users.sql
touch agentic-ai-sql-project/src/dbt/models/marts/core/dim_users.sql
touch agentic-ai-sql-project/src/dbt/models/marts/core/fct_events.sql
touch agentic-ai-sql-project/src/dbt/models/marts/analytics/user_sessions.sql
touch agentic-ai-sql-project/src/dbt/models/marts/analytics/ab_test_results.sql

# Configuration files
touch agentic-ai-sql-project/config/database_connections.json
touch agentic-ai-sql-project/config/tableau_config.yml
touch agentic-ai-sql-project/config/dbt_profiles.yml
touch agentic-ai-sql-project/config/sql_fluff.yml

# Documentation and tests
touch agentic-ai-sql-project/docs/data_dictionary.md
touch agentic-ai-sql-project/docs/sql_standards.md
touch agentic-ai-sql-project/docs/ab_test_framework.md

touch agentic-ai-sql-project/tests/test_sql_queries.py
touch agentic-ai-sql-project/tests/test_data_quality.py
touch agentic-ai-sql-project/tests/test_ab_analysis.py

# Tableau files
touch agentic-ai-sql-project/dashboards/product_analytics.twb
touch agentic-ai-sql-project/dashboards/ab_test_dashboard.twb
touch agentic-ai-sql-project/dashboards/data_quality_monitor.twb

echo "Agentic AI SQL Project structure created successfully!"

# Create the final tree structure
tree agentic-ai-sql-project -I 'venv|__pycache__|*.pyc'
