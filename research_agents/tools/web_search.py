# tools/web_search.py
import json
from typing import Dict, List, Optional

import requests

from config.settings import config


class WebSearchTool:
    """Tool for performing web searches and gathering information"""

    def __init__(self):
        self.api_key = config.SERPER_API_KEY
        self.base_url = "https://google.serper.dev/search"

    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """Perform a web search and return results"""
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        payload = {
            'q': query,
            'num': num_results
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()

            results = []
            # Extract organic results
            for item in data.get('organic', []):
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'position': item.get('position', 0)
                })

            return results[:num_results]

        except Exception as e:
            print(f"Search error: {e}")
            return []

    def search_multiple_queries(self, queries: List[str]) -> Dict[str, List[Dict]]:
        """Search multiple queries and return organized results"""
        all_results = {}
        for query in queries:
            all_results[query] = self.search(query)
        return all_results
