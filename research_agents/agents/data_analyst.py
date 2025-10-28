# agents/data_analyst.py
from typing import Any, Dict, List

import openai

from config.settings import config


class DataAnalyst:
    """Agent responsible for analyzing and interpreting research data"""

    def __init__(self):
        openai.api_key = config.OPENAI_API_KEY

    def identify_patterns(self, research_data: List[Dict]) -> Dict[str, Any]:
        """Identify patterns and trends in the research data"""
        snippets = [item.get('snippet', '') for item in research_data]
        combined_text = "\n\n".join(snippets[:20])  # Limit to first 20 snippets

        prompt = f"""
        Analyze the following research data and identify:

        1. Main themes and patterns
        2. Conflicting information or debates
        3. Consensus areas
        4. Knowledge gaps
        5. Emerging trends
        6. Key statistics or data points

        RESEARCH DATA:
        {combined_text}

        Provide a structured analysis.
        """

        response = openai.ChatCompletion.create(
            model=config.PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert data analyst. Identify patterns, trends, and insights from information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=config.MAX_TOKENS
        )

        return {
            "pattern_analysis": response.choices[0].message.content,
            "data_points_analyzed": len(research_data)
        }

    def validate_information(self, research_data: List[Dict]) -> Dict[str, Any]:
        """Assess information quality and identify potential biases"""
        sources = [item.get('link', '') for item in research_data]
        snippets = [item.get('snippet', '') for item in research_data]

        prompt = f"""
        Assess the quality and reliability of these information sources:

        SOURCES:
        {chr(10).join(f"- {src}" for src in sources[:10])}

        Assess:
        1. Source credibility
        2. Potential biases
        3. Information consistency across sources
        4. Data recency where available
        5. Overall reliability assessment

        Provide a critical evaluation.
        """

        response = openai.ChatCompletion.create(
            model=config.PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert critical thinker. Evaluate information quality and reliability."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return {
            "quality_assessment": response.choices[0].message.content,
            "sources_evaluated": len(sources)
        }
