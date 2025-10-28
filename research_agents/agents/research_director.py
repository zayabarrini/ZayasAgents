# agents/research_director.py
from typing import Dict, List, Any
import openai
from config.settings import config

class ResearchDirector:
    """Orchestrates the research process and coordinates other agents"""

    def __init__(self, topic: str):
        self.topic = topic
        self.research_plan = {}
        self.current_state = "initializing"
        self.findings = []
        openai.api_key = config.OPENAI_API_KEY

    def create_research_plan(self) -> Dict[str, Any]:
        """Create a comprehensive research plan"""
        prompt = f"""
        Create a detailed research plan for the topic: "{self.topic}"

        The plan should include:
        1. Key research questions to answer
        2. Sub-topics to investigate
        3. Specific search queries for web research
        4. Potential data sources
        5. Analysis approaches

        Return the plan as a JSON structure with these sections.
        """

        response = openai.ChatCompletion.create(
            model=config.PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert research director. Create structured, actionable research plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=config.MAX_TOKENS
        )

        plan_text = response.choices[0].message.content
        # Parse the JSON response (in a real implementation, you'd want more robust parsing)
        try:
            import json
            self.research_plan = json.loads(plan_text)
        except:
            # Fallback: create a basic structure
            self.research_plan = {
                "research_questions": [
                    f"What are the key aspects of {self.topic}?",
                    f"What are recent developments in {self.topic}?",
                    f"What are the main challenges and opportunities in {self.topic}?"
                ],
                "search_queries": [
                    f"comprehensive guide {self.topic}",
                    f"recent developments {self.topic} 2024",
                    f"future trends {self.topic}",
                    f"key challenges {self.topic}"
                ],
                "subtopics": ["background", "current_state", "future_trends", "key_players"]
            }

        self.current_state = "planning_complete"
        return self.research_plan

    def analyze_findings(self, research_data: List[Dict]) -> Dict[str, Any]:
        """Analyze and synthesize research findings"""
        all_content = "\n".join([item.get('snippet', '') for item in research_data])

        prompt = f"""
        Analyze the following research findings about "{self.topic}" and provide a comprehensive synthesis:

        RESEARCH DATA:
        {all_content[:3000]}  # Limit context length

        Provide analysis in this structure:
        1. Executive Summary
        2. Key Findings
        3. Important Statistics and Data
        4. Emerging Trends
        5. Remaining Questions
        6. Conclusions

        Be thorough and analytical.
        """

        response = openai.ChatCompletion.create(
            model=config.PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert research analyst. Synthesize information and provide insightful analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=config.MAX_TOKENS
        )

        analysis = response.choices[0].message.content
        self.findings.append(analysis)
        self.current_state = "analysis_complete"

        return {
            "analysis": analysis,
            "sources_analyzed": len(research_data),
            "key_insights": self._extract_key_insights(analysis)
        }

    def _extract_key_insights(self, analysis: str) -> List[str]:
        """Extract key insights from analysis"""
        # Simple extraction - in practice, you might use more sophisticated NLP
        lines = analysis.split('\n')
        insights = [line.strip() for line in lines if line.strip() and any(marker in line for marker in ['•', '-', '•', 'key', 'important', 'significant']))]
        return insights[:10]  # Return top 10 insights
