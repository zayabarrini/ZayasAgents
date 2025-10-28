# config/settings.py
import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the research agents"""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # For web search

    # Model Settings
    PRIMARY_MODEL = "gpt-4"
    FALLBACK_MODEL = "gpt-3.5-turbo"

    # Research Settings
    MAX_SEARCH_RESULTS = 10
    RESEARCH_DEPTH = "comprehensive"  # quick, standard, comprehensive
    MAX_TOKENS = 4000

    # Output Settings
    OUTPUT_DIR = "outputs/reports"
    REPORT_FORMAT = "markdown"  # markdown, html, pdf

    # Agent Settings
    MAX_ITERATIONS = 5
    VERBOSE = True

config = Config()
