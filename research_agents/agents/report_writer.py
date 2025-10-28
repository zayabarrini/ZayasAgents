# agents/report_writer.py
from typing import Any, Dict

import openai

from config.settings import config


class ReportWriter:
    """Agent responsible for compiling research findings into comprehensive reports"""

    def __init__(self):
        openai.api_key = config.OPENAI_API_KEY

    def generate_report(self, topic: str, research_plan: Dict, research_data: Dict, analysis: Dict) -> str:
        """Generate a comprehensive research report"""

        prompt = f"""
        Compile a comprehensive research report on: "{topic}"

        RESEARCH PLAN:
        {research_plan}

        KEY FINDINGS:
        {analysis.get('analysis', '')}

        PATTERN ANALYSIS:
        {analysis.get('pattern_analysis', '')}

        Create a well-structured report with:

        1. Executive Summary
        2. Introduction and Research Objectives
        3. Methodology
        4. Key Findings
        5. Detailed Analysis
        6. Patterns and Trends Identified
        7. Conclusions
        8. Recommendations for Further Research

        Make it professional, comprehensive, and well-organized.
        Include relevant statistics and specific insights.
        """

        response = openai.ChatCompletion.create(
            model=config.PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert technical writer. Create comprehensive, well-structured research reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=config.MAX_TOKENS * 2  # Allow more tokens for comprehensive report
        )

        return response.choices[0].message.content

    def create_executive_summary(self, full_report: str) -> str:
        """Create an executive summary from the full report"""

        prompt = f"""
        Create a concise executive summary (max 300 words) from this research report:

        {full_report[:2000]}  # Use first part of report for context

        Focus on:
        - Key findings
        - Main conclusions
        - Important recommendations

        Keep it brief and impactful.
        """

        response = openai.ChatCompletion.create(
            model=config.FALLBACK_MODEL,
            messages=[
                {"role": "system", "content": "You create concise, impactful executive summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content
