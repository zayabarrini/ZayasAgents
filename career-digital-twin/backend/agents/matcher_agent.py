# backend/agents/matcher_agent.py
import openai
import os
import re
from typing import Dict, List

class MatcherAgent:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
        openai.api_key = self.api_key
        self.profile_agent = None
    
    def set_profile_agent(self, profile_agent):
        """Set the profile agent for context"""
        self.profile_agent = profile_agent
    
    def analyze_match(self, job_description: str) -> Dict:
        """Analyze match between profile and job description"""
        if not self.profile_agent:
            return {"error": "Profile agent not configured"}
        
        profile = self.profile_agent.get_profile()
        
        prompt = self._create_analysis_prompt(profile, job_description)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            return self._parse_analysis_response(analysis_text)
        
        except Exception as e:
            return {
                "overall_match": 0,
                "breakdown": {},
                "recommendations": ["Error analyzing match. Please try again."]
            }
    
    def _create_analysis_prompt(self, profile: Dict, job_description: str) -> str:
        """Create prompt for job match analysis"""
        skills = ", ".join(profile.get('skills', []))
        
        experience_text = ""
        for exp in profile.get('experience', []):
            experience_text += f"- {exp['position']} at {exp['company']}: {exp['description']}\n"
        
        return f"""
        Analyze the match between this candidate profile and the job description below.
        
        CANDIDATE PROFILE:
        Name: {profile.get('name', 'Candidate')}
        Title: {profile.get('title', '')}
        Skills: {skills}
        Experience:
        {experience_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Please provide a detailed analysis in the following format:
        
        OVERALL_MATCH: [percentage]%
        
        BREAKDOWN:
        Skills Match: [percentage]%
        Experience Match: [percentage]%
        Education Match: [percentage]%
        Culture Fit: [percentage]%
        
        RECOMMENDATIONS:
        - [Specific recommendation 1]
        - [Specific recommendation 2]
        - [Specific recommendation 3]
        
        Focus on:
        1. How well the candidate's skills match the job requirements
        2. Relevance of the candidate's experience
        3. Any gaps and how to address them
        4. Strengths the candidate should highlight
        """
    
    def _parse_analysis_response(self, response_text: str) -> Dict:
        """Parse the LLM response into structured data"""
        result = {
            "overall_match": 0,
            "breakdown": {},
            "recommendations": []
        }
        
        # Extract overall match
        overall_match = re.search(r'OVERALL_MATCH:\s*(\d+)%', response_text)
        if overall_match:
            result["overall_match"] = int(overall_match.group(1))
        
        # Extract breakdown
        breakdown_section = re.search(r'BREAKDOWN:(.*?)RECOMMENDATIONS:', response_text, re.DOTALL)
        if breakdown_section:
            breakdown_text = breakdown_section.group(1)
            matches = re.findall(r'(\w+\s*\w+):\s*(\d+)%', breakdown_text)
            for category, percentage in matches:
                result["breakdown"][category.lower().replace(' ', '_')] = int(percentage)
        
        # Extract recommendations
        recommendations_section = re.search(r'RECOMMENDATIONS:(.*)', response_text, re.DOTALL)
        if recommendations_section:
            recommendations_text = recommendations_section.group(1)
            recommendations = re.findall(r'-\s*(.*)', recommendations_text)
            result["recommendations"] = recommendations
        
        return result