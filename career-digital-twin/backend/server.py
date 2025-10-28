# backend/server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from agents.profile_agent import ProfileAgent
from agents.interview_agent import InterviewAgent
from agents.matcher_agent import MatcherAgent

app = Flask(__name__)
CORS(app)

# Initialize agents
profile_agent = ProfileAgent()
interview_agent = InterviewAgent()
matcher_agent = MatcherAgent()

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('../frontend', path)

@app.route('/api/profile', methods=['GET'])
def get_profile():
    """Get the user's professional profile"""
    try:
        profile = profile_agent.get_profile()
        return jsonify(profile)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with the interview agent"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        chat_history = data.get('chat_history', [])
        
        response = interview_agent.respond(user_message, chat_history)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-match', methods=['POST'])
def analyze_match():
    """Analyze job match between profile and job description"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        
        match_analysis = matcher_agent.analyze_match(job_description)
        return jsonify(match_analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)