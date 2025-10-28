# mcp_servers/market_data_server.py
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import aiohttp
import logging
from typing import Dict, List, Optional, Any
import yfinance as yf

class MarketDataServer:
    def __init__(self):
        self.logger = logging.getLogger("MarketDataServer")
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
        
        # Available tools
        self.tools = {
            'get_real_time_data': self.get_real_time_data,
            'get_historical_data': self.get_historical_data,
            'get_technical_indicators': self.get_technical_indicators,
            'get_market_sentiment': self.get_market_sentiment,
            'get_news_sentiment': self.get_news_sentiment,
            'get_volatility_metrics': self.get_volatility_metrics,
            'get_correlation_matrix': self.get_correlation_matrix,
            'get_sector_performance': self.get_sector_performance
        }
    
    async def get_real_time_data(self, symbols: List[str] = None) -> Dict[str, pd.DataFrame]:
        """Get real-time market data for symbols"""
        if symbols is None:
            symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'SPY']  # Default symbols
        
        real_time_data = {}
        
        for symbol in symbols:
            try:
                # Check cache first
                cache_key = f"realtime_{symbol}"
                if (cache_key in self.cache and 
                    datetime.now() - self.cache[cache_key]['timestamp'] < self.cache_duration):
                    real_time_data[symbol] = self.cache[cache_key]['data']
                    continue
                
                # Fetch from yfinance
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1mo", interval="1d")
                
                if not hist.empty:
                    # Add some simulated real-time data
                    latest = hist.iloc[-1].copy()
                    # Simulate intraday movement
                    movement = np.random.normal(0, latest['Close'] * 0.01)
                    latest['Close'] += movement
                    latest['High'] = max(latest['High'], latest['Close'])
                    latest['Low'] = min(latest['Low'], latest['Close'])
                    
                    real_time_data[symbol] = hist
                    
                    # Update cache
                    self.cache[cache_key] = {
                        'data': hist,
                        'timestamp': datetime.now()
                    }
                    
            except Exception as e:
                self.logger.error(f"Error fetching data for {symbol}: {e}")
                continue
        
        return real_time_data
    
    async def get_historical_data(self, symbol: str, period: str = "1y", 
                                interval: str = "1d") -> pd.DataFrame:
        """Get historical price data"""
        try:
            ticker = yf.Ticker(symbol)
            hist_data = ticker.history(period=period, interval=interval)
            return hist_data
        except Exception as e:
            self.logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    async def get_technical_indicators(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate technical indicators"""
        import talib
        
        closes = data['Close'].values
        highs = data['High'].values
        lows = data['Low'].values
        volumes = data['Volume'].values
        
        indicators = {}
        
        try:
            # Moving averages
            indicators['sma_20'] = talib.SMA(closes, timeperiod=20)[-1]
            indicators['sma_50'] = talib.SMA(closes, timeperiod=50)[-1]
            indicators['ema_12'] = talib.EMA(closes, timeperiod=12)[-1]
            indicators['ema_26'] = talib.EMA(closes, timeperiod=26)[-1]
            
            # Oscillators
            indicators['rsi'] = talib.RSI(closes, timeperiod=14)[-1]
            macd, macd_signal, macd_hist = talib.MACD(closes)
            indicators['macd'] = macd[-1]
            indicators['macd_signal'] = macd_signal[-1]
            indicators['macd_hist'] = macd_hist[-1]
            
            # Volatility
            indicators['atr'] = talib.ATR(highs, lows, closes, timeperiod=14)[-1]
            bb_upper, bb_middle, bb_lower = talib.BBANDS(closes, timeperiod=20)
            indicators['bb_upper'] = bb_upper[-1]
            indicators['bb_lower'] = bb_lower[-1]
            indicators['bb_middle'] = bb_middle[-1]
            
            # Volume
            indicators['obv'] = talib.OBV(closes, volumes)[-1]
            
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators: {e}")
        
        return indicators
    
    async def get_market_sentiment(self, symbol: str) -> Dict[str, float]:
        """Get market sentiment for symbol"""
        # This would typically integrate with sentiment analysis APIs
        # For now, return simulated sentiment data
        return {
            'bullish_ratio': np.random.uniform(0.3, 0.7),
            'sentiment_score': np.random.uniform(-1, 1),
            'news_sentiment': np.random.uniform(-0.5, 0.5),
            'social_sentiment': np.random.uniform(-0.8, 0.8)
        }
    
    async def get_news_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Get news-based sentiment"""
        # Simulated news sentiment
        return {
            'recent_news_count': np.random.randint(5, 50),
            'positive_news_ratio': np.random.uniform(0.2, 0.8),
            'overall_sentiment': np.random.uniform(-0.5, 0.5),
            'key_topics': ['earnings', 'analyst_ratings', 'market_trends']
        }
    
    async def get_volatility_metrics(self, symbol: str, lookback_days: int = 30) -> Dict[str, float]:
        """Calculate volatility metrics"""
        try:
            data = await self.get_historical_data(symbol, period=f"{lookback_days}d")
            returns = data['Close'].pct_change().dropna()
            
            return {
                'historical_volatility': returns.std() * np.sqrt(252),
                'avg_true_range': await self.calculate_atr(data),
                'volatility_ratio': returns.std() / returns.abs().mean(),
                'max_drawdown': await self.calculate_max_drawdown(data['Close'])
            }
        except Exception as e:
            self.logger.error(f"Error calculating volatility for {symbol}: {e}")
            return {}
    
    async def calculate_atr(self, data: pd.DataFrame) -> float:
        """Calculate Average True Range"""
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        return true_range.mean()
    
    async def calculate_max_drawdown(self, prices: pd.Series) -> float:
        """Calculate maximum drawdown"""
        peak = prices.expanding().max()
        drawdown = (prices - peak) / peak
        return drawdown.min()
    
    async def get_correlation_matrix(self, symbols: List[str]) -> pd.DataFrame:
        """Get correlation matrix for symbols"""
        try:
            data = {}
            for symbol in symbols:
                hist_data = await self.get_historical_data(symbol, period="6mo")
                if not hist_data.empty:
                    data[symbol] = hist_data['Close']
            
            df = pd.DataFrame(data)
            returns = df.pct_change().dropna()
            correlation_matrix = returns.corr()
            
            return correlation_matrix
            
        except Exception as e:
            self.logger.error(f"Error calculating correlation matrix: {e}")
            return pd.DataFrame()
    
    async def get_sector_performance(self) -> Dict[str, float]:
        """Get sector performance data"""
        # Simulated sector performance
        sectors = ['Technology', 'Healthcare', 'Financials', 'Energy', 
                  'Consumer Discretionary', 'Industrials', 'Utilities']
        
        return {sector: np.random.uniform(-0.05, 0.05) for sector in sectors}