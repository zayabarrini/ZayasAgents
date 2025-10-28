#!/bin/bash
mkdir -p research_agents/{agents,tools,config,outputs/reports}
touch research_agents/__init__.py research_agents/main.py
touch research_agents/agents/__init__.py research_agents/agents/research_director.py research_agents/agents/web_researcher.py research_agents/agents/data_analyst.py research_agents/agents/report_writer.py
touch research_agents/tools/__init__.py research_agents/tools/web_search.py research_agents/tools/data_processor.py research_agents/tools/file_manager.py
touch research_agents/config/__init__.py research_agents/config/settings.py
touch research_agents/outputs/__init__.py
touch research_agents/.env.example research_agents/requirements.txt research_agents/README.md research_agents/.gitignore research_agents/setup.py
echo "Research agents project structure created successfully!"
