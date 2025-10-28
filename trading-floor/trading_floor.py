# trading_floor.py
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import logging
from dataclasses import dataclass
from enum import Enum

class AssetClass(Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    FOREX = "forex"
    FUTURES = "futures"

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

@dataclass
class TradeSignal:
    symbol: str
    action: str  # BUY, SELL, HOLD
    confidence: float
    price_target: float
    stop_loss: float
    quantity: int
    asset_class: AssetClass
    timestamp: datetime

@dataclass
class Position:
    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    pnl: float
    timestamp: datetime

class TradingFloor:
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.available_capital = initial_capital
        self.positions: Dict[str, Position] = {}
        self.trade_history = []
        self.agents = {}
        self.mcp_servers = {}
        self.performance_metrics = {}
        
        # Initialize components
        self.setup_logging()
        self.initialize_agents()
        self.initialize_mcp_servers()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_floor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("TradingFloor")
    
    def initialize_agents(self):
        """Initialize the 4 trading agents"""
        from market_analyzer_agent import MarketAnalyzerAgent
        from risk_manager_agent import RiskManagerAgent
        from portfolio_optimizer_agent import PortfolioOptimizerAgent
        from execution_agent import ExecutionAgent
        
        self.agents['market_analyzer'] = MarketAnalyzerAgent(self)
        self.agents['risk_manager'] = RiskManagerAgent(self)
        self.agents['portfolio_optimizer'] = PortfolioOptimizerAgent(self)
        self.agents['execution_agent'] = ExecutionAgent(self)
        
        self.logger.info("All 4 trading agents initialized")
    
    def initialize_mcp_servers(self):
        """Initialize the 6 MCP servers"""
        from mcp_servers.market_data_server import MarketDataServer
        from mcp_servers.risk_management_server import RiskManagementServer
        from mcp_servers.portfolio_analytics_server import PortfolioAnalyticsServer
        from mcp_servers.execution_engine_server import ExecutionEngineServer
        from mcp_servers.compliance_monitor_server import ComplianceMonitorServer
        from mcp_servers.performance_tracker_server import PerformanceTrackerServer
        
        self.mcp_servers['market_data'] = MarketDataServer()
        self.mcp_servers['risk_management'] = RiskManagementServer()
        self.mcp_servers['portfolio_analytics'] = PortfolioAnalyticsServer()
        self.mcp_servers['execution_engine'] = ExecutionEngineServer()
        self.mcp_servers['compliance_monitor'] = ComplianceMonitorServer()
        self.mcp_servers['performance_tracker'] = PerformanceTrackerServer()
        
        self.logger.info("All 6 MCP servers initialized")
    
    async def run_trading_cycle(self):
        """Main trading cycle"""
        self.logger.info("Starting trading cycle")
        
        # Step 1: Market Analysis
        market_signals = await self.agents['market_analyzer'].analyze_markets()
        
        # Step 2: Risk Assessment
        risk_assessment = await self.agents['risk_manager'].assess_risk(market_signals)
        
        # Step 3: Portfolio Optimization
        trading_decisions = await self.agents['portfolio_optimizer'].optimize_portfolio(
            market_signals, risk_assessment
        )
        
        # Step 4: Trade Execution
        execution_results = await self.agents['execution_agent'].execute_trades(trading_decisions)
        
        # Step 5: Update Performance
        await self.update_performance_metrics()
        
        return execution_results
    
    async def update_performance_metrics(self):
        """Update performance metrics"""
        total_value = self.available_capital
        for position in self.positions.values():
            total_value += position.quantity * position.current_price
        
        self.performance_metrics = {
            'total_portfolio_value': total_value,
            'total_pnl': total_value - self.initial_capital,
            'return_percentage': (total_value - self.initial_capital) / self.initial_capital * 100,
            'active_positions': len(self.positions),
            'last_update': datetime.now()
        }