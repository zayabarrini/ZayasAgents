# agents/web_researcher.py
from typing import Dict, List

import openai

from config.settings import config
from tools.data_processor import DataProcessor
from tools.web_search import WebSearchTool


class WebResearcher:
    """Agent responsible for gathering information from web sources"""

    def __init__(self):
        self.search_tool = WebSearchTool()
        self.data_processor = DataProcessor()
        openai.api_key = config.OPENAI_API_KEY

    def generate_search_queries(self, topic: str, research_questions: List[str]) -> List[str]:
        """Generate optimized search queries based on research questions"""
        prompt = f"""
        Generate specific, effective web search queries for researching: "{topic}"

        Research questions to answer:
        {chr(10).join(f"- {q}" for q in research_questions)}

        Provide 5-8 specific search queries that would yield comprehensive information.
        Return only the queries, one per line.
        """

        response = openai.ChatCompletion.create(
            model=config.FALLBACK_MODEL,
            messages=[
                {"role": "system", "content": "You are expert at creating effective web search queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        queries_text = response.choices[0].message.content
        queries = [q.strip() for q in queries_text.split('\n') if q.strip()]
        return queries

    def conduct_research(self, queries: List[str]) -> Dict[str, Any]:
        """Conduct comprehensive web research"""
        print(f"🔍 Conducting research with {len(queries)} queries...")

        all_results = {}
        for i, query in enumerate(queries):
            if config.VERBOSE:
                print(f"  Searching: {query}")

            results = self.search_tool.search(query, config.MAX_SEARCH_RESULTS)
            all_results[query] = results

        # Process and analyze the data
        flattened_results = []
        for query_results in all_results.values():
            flattened_results.extend(query_results)

        summary = self.data_processor.summarize_findings(flattened_results)
        key_info = self.data_processor.extract_key_information(
            " ".join([r.get('snippet', '') for r in flattened_results])
        )

        return {
            "raw_results": all_results,
            "flattened_results": flattened_results,
            "summary": summary,
            "key_information": key_info,
            "total_results": len(flattened_results)
        }
