import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config import Config

# Initialize tools
search_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()

class StockPickerCrew:
    def __init__(self):
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        
    def _create_agents(self):
        """Create specialized agents for stock analysis"""
        
        # Market Researcher Agent
        market_researcher = Agent(
            role="Senior Market Research Analyst",
            goal="Identify promising market sectors and industry trends for investment opportunities",
            backstory="""You are an experienced market research analyst with deep knowledge 
            of global markets, sector rotations, and macroeconomic trends. You excel at 
            identifying emerging opportunities before they become mainstream.""",
            tools=[search_tool, web_search_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Financial Analyst Agent
        financial_analyst = Agent(
            role="Senior Financial Analyst",
            goal="Analyze company financials, valuation metrics, and growth potential",
            backstory="""You are a CFA charterholder with 15 years of experience analyzing 
            company financial statements, valuation models, and investment metrics. You're 
            known for your rigorous financial analysis and conservative investment approach.""",
            tools=[search_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Technical Analyst Agent
        technical_analyst = Agent(
            role="Senior Technical Analyst",
            goal="Analyze stock price trends, technical indicators, and market timing",
            backstory="""You are a technical analysis expert with deep knowledge of 
            chart patterns, technical indicators, and market sentiment. You combine 
            quantitative analysis with market psychology to identify optimal entry points.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Investment Strategist Agent
        investment_strategist = Agent(
            role="Chief Investment Strategist",
            goal="Synthesize all analysis and make final investment recommendations",
            backstory="""You are the final decision maker with 20 years of portfolio 
            management experience. You weigh all factors - fundamental, technical, 
            and macroeconomic - to create balanced investment recommendations.""",
            verbose=True,
            allow_delegation=True
        )
        
        return {
            "market_researcher": market_researcher,
            "financial_analyst": financial_analyst,
            "technical_analyst": technical_analyst,
            "investment_strategist": investment_strategist
        }
    
    def _create_tasks(self):
        """Create tasks for each agent"""
        
        market_research_task = Task(
            description="""Research current market trends and identify 3-5 promising 
            sectors for investment. Focus on sectors with strong growth catalysts, 
            favorable macroeconomic conditions, and positive industry trends.
            
            For each sector, provide:
            1. Growth catalysts and drivers
            2. Key risks and challenges
            3. Top 2-3 companies to investigate further
            4. Market sentiment analysis
            
            Current date: {current_date}""",
            agent=self.agents["market_researcher"],
            expected_output="Comprehensive market sector analysis with specific company recommendations"
        )
        
        financial_analysis_task = Task(
            description="""For the companies identified by the market researcher, 
            conduct deep financial analysis. Analyze:
            
            For each company:
            1. Revenue growth trends (3-5 years)
            2. Profitability margins (Gross, Operating, Net)
            3. Debt-to-Equity ratio and financial health
            4. Valuation metrics (P/E, P/S, EV/EBITDA)
            5. Return on Equity and Capital
            6. Free Cash Flow generation
            
            Filter out companies that don't meet:
            - Positive earnings growth
            - Reasonable valuation (P/E < 30)
            - Strong balance sheet
            - Consistent free cash flow
            
            Current date: {current_date}""",
            agent=self.agents["financial_analyst"],
            expected_output="Detailed financial analysis report with buy/hold/sell recommendations",
            context=[market_research_task]
        )
        
        technical_analysis_task = Task(
            description="""For the financially sound companies identified, conduct 
            technical analysis:
            
            For each stock:
            1. Price trend analysis (1-year chart)
            2. Key support and resistance levels
            3. Moving averages (50-day, 200-day)
            4. Relative Strength Index (RSI)
            5. Trading volume analysis
            6. Chart patterns and breakouts
            
            Identify stocks that are:
            - In uptrends or showing bullish patterns
            - Not overbought (RSI < 70)
            - Above key moving averages
            - Showing strong volume support
            
            Current date: {current_date}""",
            agent=self.agents["technical_analyst"],
            expected_output="Technical analysis report with entry/exit points and risk levels",
            context=[financial_analysis_task]
        )
        
        investment_recommendation_task = Task(
            description="""Synthesize all previous analyses and create final 
            investment recommendations:
            
            Create a portfolio of 3-5 stocks with:
            1. Specific buy recommendations with price targets
            2. Risk assessment for each position
            3. Position sizing recommendations
            4. Time horizon for each investment
            5. Key monitoring metrics
            6. Catalyst timeline
            
            Provide a balanced portfolio with different risk profiles and 
            investment timeframes. Include both growth and value opportunities.
            
            Format your final recommendation as:
            - Stock Ticker
            - Company Name
            - Sector
            - Recommendation (Strong Buy/Buy/Hold)
            - Target Price
            - Current Price
            - Upside Potential
            - Risk Level (Low/Medium/High)
            - Investment Timeframe
            - Key Catalysts
            
            Current date: {current_date}""",
            agent=self.agents["investment_strategist"],
            expected_output="Final investment recommendation report with specific buy recommendations",
            context=[market_research_task, financial_analysis_task, technical_analysis_task]
        )
        
        return {
            "market_research": market_research_task,
            "financial_analysis": financial_analysis_task,
            "technical_analysis": technical_analysis_task,
            "investment_recommendation": investment_recommendation_task
        }
    
    def get_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Get real stock data using yfinance"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            prev_close = info.get('regularMarketPreviousClose', current_price)
            
            return {
                'ticker': ticker,
                'company_name': info.get('longName', ticker),
                'sector': info.get('sector', 'N/A'),
                'current_price': current_price,
                'previous_close': prev_close,
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'volume': info.get('volume', 0),
                'price_change': current_price - prev_close,
                'price_change_pct': ((current_price - prev_close) / prev_close) * 100,
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0)
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
    
    def run_analysis(self, custom_tickers: List[str] = None):
        """Run the complete stock analysis"""
        print("🚀 Starting Stock Picker Agent Analysis...")
        print("=" * 60)
        
        # Get current date for context
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Update tasks with current date
        for task in self.tasks.values():
            task.description = task.description.format(current_date=current_date)
        
        # Create and run the crew
        stock_crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            process=Process.sequential,
            verbose=True
        )
        
        print("🧠 CrewAI agents are analyzing the market...")
        result = stock_crew.kickoff()
        
        print("\n" + "=" * 60)
        print("📊 FINAL INVESTMENT RECOMMENDATIONS")
        print("=" * 60)
        print(result)
        
        # If we have custom tickers, show real data
        if custom_tickers:
            print("\n" + "=" * 60)
            print("📈 REAL-TIME STOCK DATA")
            print("=" * 60)
            for ticker in custom_tickers:
                data = self.get_stock_data(ticker)
                if data:
                    print(f"\n{ticker}: {data['company_name']}")
                    print(f"  Price: ${data['current_price']:.2f}")
                    print(f"  Change: {data['price_change_pct']:+.2f}%")
                    print(f"  Sector: {data['sector']}")
                    print(f"  P/E Ratio: {data['pe_ratio']:.2f}")
        
        return result

def main():
    """Main function to run the stock picker"""
    
    # Check for OpenAI API key
    if not Config.OPENAI_API_KEY:
        print("❌ Please set OPENAI_API_KEY in your environment variables")
        return
    
    # Initialize the stock picker crew
    stock_picker = StockPickerCrew()
    
    # Optional: Add specific tickers you want to analyze
    custom_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    
    # Run the analysis
    try:
        recommendations = stock_picker.run_analysis(custom_tickers)
        
        # Save results to file
        with open("investment_recommendations.txt", "w") as f:
            f.write(f"Stock Picker Agent Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 50 + "\n")
            f.write(str(recommendations))
            
        print(f"\n💾 Recommendations saved to 'investment_recommendations.txt'")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    main()