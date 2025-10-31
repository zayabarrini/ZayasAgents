#!/bin/bash

# Create the main project directory
mkdir -p international-payments

# Create src directory and subdirectories
mkdir -p international-payments/src/{config,core,agents,services,regional,api,utils}

# Create tests directory structure
mkdir -p international-payments/tests/{unit,integration,fixtures}

# Create other top-level directories
mkdir -p international-payments/{docs,requirements,scripts,configs}

# Create all __init__.py files
touch international-payments/src/__init__.py
touch international-payments/src/config/__init__.py
touch international-payments/src/core/__init__.py
touch international-payments/src/agents/__init__.py
touch international-payments/src/services/__init__.py
touch international-payments/src/regional/__init__.py
touch international-payments/src/api/__init__.py
touch international-payments/src/utils/__init__.py
touch international-payments/tests/__init__.py

# Create Python files in src directory
touch international-payments/src/main.py
touch international-payments/src/config/settings.py
touch international-payments/src/config/constants.py
touch international-payments/src/core/payment_processor.py
touch international-payments/src/core/security_manager.py
touch international-payments/src/core/models.py
touch international-payments/src/core/exceptions.py
touch international-payments/src/agents/payment_agent.py
touch international-payments/src/agents/fraud_detector.py
touch international-payments/src/agents/route_optimizer.py
touch international-payments/src/services/exchange_service.py
touch international-payments/src/services/compliance_service.py
touch international-payments/src/services/analytics_service.py
touch international-payments/src/services/notification_service.py
touch international-payments/src/regional/compliance_rules.py
touch international-payments/src/regional/currency_rules.py
touch international-payments/src/regional/localization.py
touch international-payments/src/api/routes.py
touch international-payments/src/api/schemas.py
touch international-payments/src/api/middleware.py
touch international-payments/src/utils/logger.py
touch international-payments/src/utils/validators.py
touch international-payments/src/utils/helpers.py

# Create documentation files
touch international-payments/docs/api.md
touch international-payments/docs/security.md
touch international-payments/docs/deployment.md

# Create requirements files
touch international-payments/requirements/base.txt
touch international-payments/requirements/dev.txt
touch international-payments/requirements/prod.txt

# Create script files
touch international-payments/scripts/deploy.sh
touch international-payments/scripts/migrate.py
touch international-payments/scripts/health_check.py

# Create configuration files
touch international-payments/configs/dev.yaml
touch international-payments/configs/staging.yaml
touch international-payments/configs/prod.yaml

# Make scripts executable
chmod +x international-payments/scripts/deploy.sh

echo "International payments project structure created successfully!"
echo "Location: $(pwd)/international-payments"