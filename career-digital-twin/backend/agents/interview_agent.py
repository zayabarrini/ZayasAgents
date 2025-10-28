# backend/agents/interview_agent.py
import openai
import os
from typing import List, Dict

class InterviewAgent:
    def __init__(self):
        # Initialize with your preferred LLM API
        self.api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
        openai.api_key = self.api_key
        self.profile_agent = None  # Will be set by main app
    
    def set_profile_agent(self, profile_agent):
        """Set the profile agent for context"""
        self.profile_agent = profile_agent
    
    def respond(self, user_message: str, chat_history: List[Dict]) -> str:
        """Generate response based on user message and profile context"""
        if not self.profile_agent:
            return "Profile agent not configured."
        
        profile = self.profile_agent.get_profile()
        
        # Create system prompt with profile context
        system_prompt = self._create_system_prompt(profile)
        
        # Prepare messages for the LLM
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history
        for msg in chat_history[-6:]:  # Keep last 6 messages for context
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"I apologize, but I'm having trouble responding right now. Error: {str(e)}"
    
    def _create_system_prompt(self, profile: Dict) -> str:
        """Create system prompt with profile information"""
        skills = ", ".join(profile.get('skills', []))
        
        experience_text = ""
        for exp in profile.get('experience', []):
            experience_text += f"- {exp['position']} at {exp['company']} ({exp['start_date']} to {exp.get('end_date', 'Present')})\n"
        
        education_text = ""
        for edu in profile.get('education', []):
            education_text += f"- {edu['degree']} from {edu['institution']} ({edu['year']})\n"
        
        return f"""
        You are a Career Digital Twin representing {profile.get('name', 'the candidate')}. 
        Your role is to answer questions about the candidate's professional background, skills, and experience.
        
        About {profile.get('name', 'the candidate')}:
        - Title: {profile.get('title', 'Professional')}
        - About: {profile.get('about', '')}
        - Key Skills: {skills}
        
        Professional Experience:
        {experience_text}
        
        Education:
        {education_text}
        
        Guidelines:
        1. Be professional, confident, and authentic
        2. Provide specific examples from the candidate's experience when relevant
        3. Focus on achievements and measurable results
        4. If you don't know something, be honest but suggest how the candidate could address similar challenges
        5. Keep responses concise but informative
        6. Always represent the candidate in the best possible light while being truthful
        """