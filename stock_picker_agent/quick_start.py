from main import StockPickerCrew
import os

def quick_analysis():
    """Quick analysis with pre-defined parameters"""
    print("🔍 Running Quick Stock Analysis...")
    
    picker = StockPickerCrew()
    
    # Focus on specific sectors or themes
    quick_tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA"]
    
    results = picker.run_analysis(quick_tickers)
    return results

if __name__ == "__main__":
    quick_analysis()