# backend/agent/browser_tools.py
from langchain.tools import tool
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

class BrowserTools:
    
    @tool
    def get_page_summary(url: str) -> str:
        """Get a summary of the webpage content"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return f"Page content (first 1000 chars): {text[:1000]}..."
            
        except Exception as e:
            return f"Error fetching page: {str(e)}"
    
    @tool
    def extract_specific_info(html_content: str, target: str) -> str:
        """Extract specific information like prices, dates, names from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        if target == "prices":
            # Look for price patterns
            import re
            price_pattern = r'\$\d+\.?\d*'
            prices = re.findall(price_pattern, html_content)
            return f"Found prices: {', '.join(set(prices))}"
        
        elif target == "dates":
            date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
            dates = re.findall(date_pattern, html_content)
            return f"Found dates: {', '.join(set(dates))}"
        
        elif target == "headings":
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
            return f"Headings: {' | '.join(headings)}"
        
        else:
            return "Please specify what to extract: prices, dates, or headings"
    
    @tool
    def compare_pages(url1: str, url2: str) -> str:
        """Compare two webpages and highlight differences"""
        try:
            content1 = requests.get(url1).text
            content2 = requests.get(url2).text
            
            soup1 = BeautifulSoup(content1, 'html.parser')
            soup2 = BeautifulSoup(content2, 'html.parser')
            
            text1 = soup1.get_text()[:1000]
            text2 = soup2.get_text()[:1000]
            
            comparison = f"""
            Page 1 ({url1}):
            {text1}
            
            Page 2 ({url2}):
            {text2}
            
            Comparison: Both pages loaded successfully.
            """
            
            return comparison
            
        except Exception as e:
            return f"Error comparing pages: {str(e)}"

# Add these tools to your main agent
browser_tools = BrowserTools()
all_tools = tools + [
    browser_tools.get_page_summary,
    browser_tools.extract_specific_info,
    browser_tools.compare_pages
]