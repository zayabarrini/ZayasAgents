#!/bin/bash

# Create project structure
echo "Setting up Research Agents project..."

# Create directories
mkdir -p research_agents/{agents,tools,config,outputs/reports} tests .vscode

# Create Python files
touch research_agents/__init__.py
touch research_agents/main.py

touch research_agents/agents/__init__.py
touch research_agents/agents/{research_director,web_researcher,data_analyst,report_writer}.py

touch research_agents/tools/__init__.py
touch research_agents/tools/{web_search,data_processor,file_manager}.py

touch research_agents/config/__init__.py
touch research_agents/config/settings.py

touch research_agents/outputs/__init__.py
touch research_agents/outputs/reports/.gitkeep

# Create configuration files
cat > .pre-commit-config.yaml << 'EOF'
# Pre-commit configuration (as above)
EOF

cat > .vscode/settings.json << 'EOF'
# VS Code settings (as above)
EOF

cat > requirements-dev.txt << 'EOF'
# Development dependencies (as above)
EOF

# Create virtual environment
python -m venv venv
echo "Virtual environment created."

echo "Project structure created!"
echo "Next steps:"
echo "1. source venv/bin/activate  # Activate virtual environment"
echo "2. pip install -r requirements-dev.txt"
echo "3. pre-commit install"
echo "4. Add your API keys to .env file"
