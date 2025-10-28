# market_analyzer_agent.py
import talib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio
from typing import List, Dict, Any
import logging

class MarketAnalyzerAgent:
    def __init__(self, trading_floor):
        self.trading_floor = trading_floor
        self.logger = logging.getLogger("MarketAnalyzerAgent")
        self.technical_indicators = [
            'RSI', 'MACD', 'BBANDS', 'STOCH', 'ATR', 
            'ADX', 'CCI', 'MFI', 'OBV', 'WILLR'
        ]
    
    async def analyze_markets(self) -> List[TradeSignal]:
        """Analyze market conditions and generate trading signals"""
        self.logger.info("Starting market analysis")
        
        # Get market data from MCP server
        market_data = await self.trading_floor.mcp_servers['market_data'].get_real_time_data()
        
        signals = []
        
        for symbol, data in market_data.items():
            signal = await self.analyze_symbol(symbol, data)
            if signal:
                signals.append(signal)
        
        self.logger.info(f"Generated {len(signals)} trading signals")
        return signals
    
    async def analyze_symbol(self, symbol: str, market_data: pd.DataFrame) -> Optional[TradeSignal]:
        """Analyze individual symbol"""
        try:
            # Technical Analysis
            tech_analysis = await self.perform_technical_analysis(market_data)
            
            # Pattern Recognition
            patterns = await self.detect_patterns(market_data)
            
            # Sentiment Analysis (using MCP server)
            sentiment = await self.trading_floor.mcp_servers['market_data'].get_sentiment_analysis(symbol)
            
            # Generate signal
            signal = await self.generate_trading_signal(
                symbol, tech_analysis, patterns, sentiment, market_data
            )
            
            return signal
            
        except Exception as e:
            self.logger.error(f"Error analyzing {symbol}: {e}")
            return None
    
    async def perform_technical_analysis(self, data: pd.DataFrame) -> Dict[str, float]:
        """Perform comprehensive technical analysis"""
        closes = data['close'].values
        highs = data['high'].values
        lows = data['low'].values
        volumes = data['volume'].values
        
        analysis = {}
        
        # RSI
        analysis['rsi'] = talib.RSI(closes, timeperiod=14)[-1]
        
        # MACD
        macd, macd_signal, macd_hist = talib.MACD(closes)
        analysis['macd'] = macd[-1]
        analysis['macd_signal'] = macd_signal[-1]
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = talib.BBANDS(closes, timeperiod=20)
        analysis['bb_position'] = (closes[-1] - bb_lower[-1]) / (bb_upper[-1] - bb_lower[-1])
        
        # Stochastic
        slowk, slowd = talib.STOCH(highs, lows, closes)
        analysis['stoch_k'] = slowk[-1]
        analysis['stoch_d'] = slowd[-1]
        
        # ATR for volatility
        analysis['atr'] = talib.ATR(highs, lows, closes, timeperiod=14)[-1]
        
        return analysis
    
    async def detect_patterns(self, data: pd.DataFrame) -> List[str]:
        """Detect candlestick patterns"""
        patterns = []
        opens = data['open'].values
        highs = data['high'].values
        lows = data['low'].values
        closes = data['close'].values
        
        # Common candlestick patterns
        pattern_functions = [
            talib.CDL2CROWS, talib.CDL3BLACKCROWS, talib.CDL3INSIDE,
            talib.CDL3LINESTRIKE, talib.CDL3OUTSIDE, talib.CDL3STARSINSOUTH,
            talib.CDL3WHITESOLDIERS, talib.CDLABANDONEDBABY, talib.CDLDOJI,
            talib.CDLENGULFING, talib.CDLHAMMER, talib.CDLHARAMI
        ]
        
        for pattern_func in pattern_functions:
            result = pattern_func(opens, highs, lows, closes)
            if result[-1] != 0:
                patterns.append(pattern_func.__name__)
        
        return patterns
    
    async def generate_trading_signal(self, symbol: str, tech_analysis: Dict, 
                                    patterns: List[str], sentiment: Dict, 
                                    data: pd.DataFrame) -> TradeSignal:
        """Generate trading signal based on analysis"""
        
        # Signal scoring system
        score = 0
        confidence_factors = []
        
        # RSI based signal
        if tech_analysis['rsi'] < 30:
            score += 2  # Oversold - bullish
            confidence_factors.append("RSI oversold")
        elif tech_analysis['rsi'] > 70:
            score -= 2  # Overbought - bearish
            confidence_factors.append("RSI overbought")
        
        # MACD signal
        if tech_analysis['macd'] > tech_analysis['macd_signal']:
            score += 1
            confidence_factors.append("MACD bullish")
        else:
            score -= 1
            confidence_factors.append("MACD bearish")
        
        # Bollinger Bands position
        if tech_analysis['bb_position'] < 0.2:
            score += 1  # Near lower band - bullish
            confidence_factors.append("Near BB lower band")
        elif tech_analysis['bb_position'] > 0.8:
            score -= 1  # Near upper band - bearish
            confidence_factors.append("Near BB upper band")
        
        # Pattern recognition
        bullish_patterns = ['CDL3WHITESOLDIERS', 'CDLHAMMER', 'CDLENGULFING']
        bearish_patterns = ['CDL3BLACKCROWS', 'CDL2CROWS']
        
        for pattern in patterns:
            if pattern in bullish_patterns:
                score += 1
                confidence_factors.append(f"Bullish pattern: {pattern}")
            elif pattern in bearish_patterns:
                score -= 1
                confidence_factors.append(f"Bearish pattern: {pattern}")
        
        # Determine action based on score
        current_price = data['close'].iloc[-1]
        
        if score >= 3:
            action = "BUY"
            confidence = min(0.9, 0.5 + (score * 0.1))
            price_target = current_price * 1.05  # 5% target
            stop_loss = current_price * 0.95     # 5% stop loss
        elif score <= -3:
            action = "SELL"
            confidence = min(0.9, 0.5 + (abs(score) * 0.1))
            price_target = current_price * 0.95  # 5% target
            stop_loss = current_price * 1.05     # 5% stop loss
        else:
            action = "HOLD"
            confidence = 0.3
            price_target = current_price
            stop_loss = current_price * 0.98
        
        # Calculate position size (simplified)
        quantity = await self.calculate_position_size(confidence, current_price)
        
        return TradeSignal(
            symbol=symbol,
            action=action,
            confidence=confidence,
            price_target=price_target,
            stop_loss=stop_loss,
            quantity=quantity,
            asset_class=AssetClass.STOCK,  # Default, should be determined
            timestamp=datetime.now()
        )
    
    async def calculate_position_size(self, confidence: float, price: float) -> int:
        """Calculate position size based on confidence and available capital"""
        max_position_size = self.trading_floor.available_capital * 0.1  # Max 10% per trade
        position_size = max_position_size * confidence
        quantity = int(position_size / price)
        return max(1, quantity)  # At least 1 share