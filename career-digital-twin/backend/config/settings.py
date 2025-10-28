# backend/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PROFILE_DATA_PATH = '../data/sample_profile.json'