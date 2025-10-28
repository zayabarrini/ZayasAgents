import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model Configuration
    MODEL_NAME = "gpt-4"
    
    # Stock Analysis Parameters
    MARKET_CAP_THRESHOLD = 1e9  # $1B minimum market cap
    VOLUME_THRESHOLD = 100000   # Minimum daily volume
    
    # Sectors to analyze
    SECTORS = [
        "Technology",
        "Healthcare", 
        "Financial Services",
        "Consumer Cyclical",
        "Industrial"
    ]