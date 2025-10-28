import yfinance as yf
import pandas as pd
from datetime import datetime

class EnhancedStockAnalysis:
    def __init__(self):
        self.risk_free_rate = 0.04  # Assume 4% risk-free rate
        
    def calculate_metrics(self, ticker: str):
        """Calculate advanced financial metrics"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="3y")
            
            # Basic metrics
            current_price = info.get('currentPrice', 0)
            market_cap = info.get('marketCap', 0)
            pe_ratio = info.get('trailingPE', 0)
            
            # Advanced metrics
            beta = info.get('beta', 1.0)
            debt_to_equity = info.get('debtToEquity', 0)
            return_on_equity = info.get('returnOnEquity', 0)
            
            # Calculate volatility (standard deviation of returns)
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std() * (252 ** 0.5)  # Annualized
            
            # Sharpe ratio (simplified)
            sharpe_ratio = (returns.mean() * 252 - self.risk_free_rate) / volatility
            
            return {
                'ticker': ticker,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'beta': beta,
                'debt_to_equity': debt_to_equity,
                'return_on_equity': return_on_equity,
                'analysis_date': datetime.now().strftime("%Y-%m-%d")
            }
        except Exception as e:
            print(f"Error in enhanced analysis for {ticker}: {e}")
            return None

# Usage example
if __name__ == "__main__":
    enhanced = EnhancedStockAnalysis()
    
    # Test with popular stocks
    test_tickers = ["AAPL", "MSFT", "TSLA", "NVDA"]
    
    for ticker in test_tickers:
        metrics = enhanced.calculate_metrics(ticker)
        if metrics:
            print(f"\n{ticker} Advanced Metrics:")
            for key, value in metrics.items():
                print(f"  {key}: {value}")