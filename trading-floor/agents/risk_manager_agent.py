# risk_manager_agent.py
import numpy as np
import pandas as pd
from datetime import datetime
import logging
from typing import Dict, List, Tuple

class RiskManagerAgent:
    def __init__(self, trading_floor):
        self.trading_floor = trading_floor
        self.logger = logging.getLogger("RiskManagerAgent")
        
        # Risk parameters
        self.max_drawdown = 0.10  # 10% maximum drawdown
        self.max_position_size = 0.10  # 10% of portfolio per position
        self.max_sector_exposure = 0.25  # 25% per sector
        self.daily_loss_limit = 0.02  # 2% daily loss limit
        
    async def assess_risk(self, signals: List[TradeSignal]) -> Dict[str, Any]:
        """Assess risk for trading signals"""
        self.logger.info("Starting risk assessment")
        
        risk_assessment = {
            'approved_signals': [],
            'rejected_signals': [],
            'risk_metrics': {},
            'warnings': []
        }
        
        # Get current portfolio risk metrics
        portfolio_risk = await self.calculate_portfolio_risk()
        risk_assessment['risk_metrics'].update(portfolio_risk)
        
        # Assess each signal
        for signal in signals:
            signal_risk = await self.assess_signal_risk(signal, portfolio_risk)
            
            if signal_risk['approved']:
                risk_assessment['approved_signals'].append({
                    'signal': signal,
                    'risk_adjustments': signal_risk['adjustments']
                })
            else:
                risk_assessment['rejected_signals'].append({
                    'signal': signal,
                    'rejection_reason': signal_risk['rejection_reason']
                })
        
        # Check overall portfolio limits
        portfolio_warnings = await self.check_portfolio_limits()
        risk_assessment['warnings'].extend(portfolio_warnings)
        
        self.logger.info(f"Risk assessment complete: {len(risk_assessment['approved_signals'])} approved, "
                        f"{len(risk_assessment['rejected_signals'])} rejected")
        
        return risk_assessment
    
    async def calculate_portfolio_risk(self) -> Dict[str, float]:
        """Calculate current portfolio risk metrics"""
        if not self.trading_floor.positions:
            return {
                'current_drawdown': 0.0,
                'portfolio_volatility': 0.0,
                'var_95': 0.0,
                'sharpe_ratio': 0.0,
                'max_position_concentration': 0.0
            }
        
        # Calculate current portfolio value
        portfolio_value = self.trading_floor.available_capital
        position_values = []
        
        for position in self.trading_floor.positions.values():
            position_value = position.quantity * position.current_price
            portfolio_value += position_value
            position_values.append(position_value)
        
        # Calculate drawdown
        peak_value = max(self.trading_floor.initial_capital, 
                        portfolio_value * 1.1)  # Simplified
        current_drawdown = (peak_value - portfolio_value) / peak_value
        
        # Calculate concentration
        if position_values:
            max_position_concentration = max(position_values) / portfolio_value
        else:
            max_position_concentration = 0.0
        
        # Get VaR from MCP server
        var_metrics = await self.trading_floor.mcp_servers['risk_management'].calculate_var(
            list(self.trading_floor.positions.values())
        )
        
        return {
            'current_drawdown': current_drawdown,
            'portfolio_volatility': var_metrics.get('volatility', 0.0),
            'var_95': var_metrics.get('var_95', 0.0),
            'sharpe_ratio': var_metrics.get('sharpe_ratio', 0.0),
            'max_position_concentration': max_position_concentration
        }
    
    async def assess_signal_risk(self, signal: TradeSignal, portfolio_risk: Dict) -> Dict[str, Any]:
        """Assess risk for individual trading signal"""
        risk_assessment = {
            'approved': True,
            'adjustments': {},
            'rejection_reason': None
        }
        
        # Check drawdown limit
        if portfolio_risk['current_drawdown'] > self.max_drawdown:
            risk_assessment['approved'] = False
            risk_assessment['rejection_reason'] = f"Max drawdown exceeded: {portfolio_risk['current_drawdown']:.2%}"
            return risk_assessment
        
        # Check position size limit
        position_value = signal.quantity * signal.price_target
        portfolio_value = self.trading_floor.available_capital + sum(
            p.quantity * p.current_price for p in self.trading_floor.positions.values()
        )
        
        position_size_ratio = position_value / portfolio_value
        
        if position_size_ratio > self.max_position_size:
            # Adjust quantity to meet position size limit
            max_position_value = portfolio_value * self.max_position_size
            adjusted_quantity = int(max_position_value / signal.price_target)
            
            if adjusted_quantity >= 1:
                risk_assessment['adjustments']['quantity'] = adjusted_quantity
                self.logger.info(f"Adjusted position size for {signal.symbol}: {signal.quantity} -> {adjusted_quantity}")
            else:
                risk_assessment['approved'] = False
                risk_assessment['rejection_reason'] = "Position size too small after risk adjustment"
                return risk_assessment
        
        # Check sector exposure (simplified)
        sector_exposure = await self.calculate_sector_exposure(signal)
        if sector_exposure > self.max_sector_exposure:
            risk_assessment['approved'] = False
            risk_assessment['rejection_reason'] = f"Sector exposure limit exceeded: {sector_exposure:.2%}"
            return risk_assessment
        
        # Check liquidity (using MCP server)
        liquidity_metrics = await self.trading_floor.mcp_servers['risk_management'].check_liquidity(
            signal.symbol, signal.quantity
        )
        
        if not liquidity_metrics.get('sufficient_liquidity', True):
            risk_assessment['approved'] = False
            risk_assessment['rejection_reason'] = "Insufficient liquidity for trade size"
            return risk_assessment
        
        return risk_assessment
    
    async def calculate_sector_exposure(self, signal: TradeSignal) -> float:
        """Calculate sector exposure for a symbol"""
        # This would typically use a sector classification service
        # For now, using a simplified approach
        sector_info = await self.trading_floor.mcp_servers['market_data'].get_sector_info(signal.symbol)
        sector = sector_info.get('sector', 'Unknown')
        
        # Calculate current sector exposure
        sector_exposure = 0.0
        total_portfolio_value = self.trading_floor.available_capital
        
        for position in self.trading_floor.positions.values():
            position_sector = await self.trading_floor.mcp_servers['market_data'].get_sector_info(position.symbol)
            if position_sector.get('sector') == sector:
                position_value = position.quantity * position.current_price
                sector_exposure += position_value
                total_portfolio_value += position_value
        
        # Add new position
        new_position_value = signal.quantity * signal.price_target
        new_sector_exposure = sector_exposure + new_position_value
        new_total_value = total_portfolio_value + new_position_value
        
        return new_sector_exposure / new_total_value if new_total_value > 0 else 0.0
    
    async def check_portfolio_limits(self) -> List[str]:
        """Check overall portfolio risk limits"""
        warnings = []
        
        portfolio_risk = await self.calculate_portfolio_risk()
        
        # Check drawdown
        if portfolio_risk['current_drawdown'] > self.max_drawdown * 0.8:  # 80% of limit
            warnings.append(f"Drawdown approaching limit: {portfolio_risk['current_drawdown']:.2%}")
        
        # Check concentration
        if portfolio_risk['max_position_concentration'] > self.max_position_size * 0.8:
            warnings.append(f"Position concentration high: {portfolio_risk['max_position_concentration']:.2%}")
        
        # Check VaR
        if portfolio_risk['var_95'] > self.trading_floor.available_capital * 0.05:  # 5% of capital
            warnings.append(f"VaR exceeding comfort level: {portfolio_risk['var_95']:.2f}")
        
        return warnings