#!/bin/bash
mkdir -p trading-floor/{agents,mcp_servers,config,data/{market_data,portfolio_data,risk_data,performance_reports},logs,utils,tests}
cd trading-floor

touch __init__.py main.py trading_floor.py requirements.txt config.py .env.example README.md

touch agents/__init__.py agents/market_analyzer_agent.py agents/risk_manager_agent.py agents/portfolio_optimizer_agent.py agents/execution_agent.py agents/base_agent.py

touch mcp_servers/__init__.py mcp_servers/market_data_server.py mcp_servers/risk_management_server.py mcp_servers/portfolio_analytics_server.py mcp_servers/execution_engine_server.py mcp_servers/compliance_monitor_server.py mcp_servers/performance_tracker_server.py mcp_servers/base_server.py

touch utils/__init__.py utils/data_processor.py utils/logger.py utils/constants.py utils/helpers.py

touch tests/__init__.py tests/test_agents.py tests/test_mcp_servers.py tests/test_integration.py tests/conftest.py

touch config/__init__.py config/settings.py config/risk_parameters.py config/trading_pairs.py

echo "Trading Floor structure created successfully!"
