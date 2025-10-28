# backend/agents/profile_agent.py
import json
import os

class ProfileAgent:
    def __init__(self, profile_path='../data/sample_profile.json'):
        self.profile_path = profile_path
        self.profile = self.load_profile()
    
    def load_profile(self):
        """Load profile data from JSON file"""
        try:
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_profile()
    
    def get_default_profile(self):
        """Return a default profile structure"""
        return {
            "name": "John Doe",
            "title": "AI Engineer",
            "about": "Passionate AI engineer with expertise in machine learning and software development.",
            "image_url": "https://via.placeholder.com/120",
            "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
            "experience": [
                {
                    "position": "Senior AI Engineer",
                    "company": "Tech Corp",
                    "start_date": "2020-01",
                    "end_date": "Present",
                    "description": "Leading AI projects and developing machine learning solutions.",
                    "achievements": [
                        "Improved model accuracy by 15%",
                        "Reduced inference time by 40%"
                    ]
                }
            ],
            "education": [
                {
                    "degree": "MSc in Computer Science",
                    "institution": "University of Technology",
                    "year": "2019",
                    "gpa": "3.8"
                }
            ]
        }
    
    def get_profile(self):
        """Return the complete profile"""
        return self.profile
    
    def update_profile(self, updates):
        """Update profile with new information"""
        self.profile.update(updates)
        self.save_profile()
        return self.profile
    
    def save_profile(self):
        """Save profile to JSON file"""
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)