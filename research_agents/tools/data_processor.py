# tools/data_processor.py
import json
import re
from collections import Counter
from typing import Any, Dict, List


class DataProcessor:
    """Tool for processing and analyzing research data"""

    @staticmethod
    def extract_key_information(text: str) -> Dict[str, Any]:
        """Extract key information from text"""
        # Extract dates
        dates = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b', text)

        # Extract numbers and statistics
        stats = re.findall(r'\b\d+%|\b\d+\.\d+%|\$\d+|\d+ million|\d+ billion', text)

        # Extract potential names (simple heuristic)
        names = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text)

        return {
            'dates': list(set(dates)),
            'statistics': list(set(stats)),
            'names': list(set(names))[:10]  # Limit to top 10
        }

    @staticmethod
    def summarize_findings(research_data: List[Dict]) -> Dict[str, Any]:
        """Summarize research findings"""
        all_snippets = [item.get('snippet', '') for item in research_data]
        all_titles = [item.get('title', '') for item in research_data]

        # Simple frequency analysis
        word_freq = Counter()
        for snippet in all_snippets:
            words = re.findall(r'\b\w+\b', snippet.lower())
            word_freq.update(words)

        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        for word in common_words:
            if word in word_freq:
                del word_freq[word]

        return {
            'total_sources': len(research_data),
            'common_themes': word_freq.most_common(10),
            'sample_titles': all_titles[:5]
        }
