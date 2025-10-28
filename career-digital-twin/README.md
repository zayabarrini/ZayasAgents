career-digital-twin/
├── frontend/
│   ├── index.html
│   ├── styles/
│   │   └── main.css
│   └── scripts/
│       └── app.js
├── backend/
│   ├── server.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── profile_agent.py
│   │   ├── interview_agent.py
│   │   └── matcher_agent.py
│   ├── models/
│   │   └── user_profile.py
│   └── config/
│       └── settings.py
├── data/
│   └── sample_profile.json
└── README.md

# Initialize project
chmod +x scripts/dev.sh
./scripts/dev.sh

# Or manually:
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
cd frontend && npm install

# Run linting
flake8 backend/
black backend/
isort backend/
npm run lint  # in frontend directory

# Start development
python backend/server.py


# Career Digital Twin - Agentic AI Engineering Project

A sophisticated AI agent that represents you to potential employers, showcasing your skills, experience, and professional capabilities.

## Features

- **Professional Profile Display**: Comprehensive view of your skills, experience, and education
- **AI-Powered Interview Agent**: Intelligent Q&A system that can answer questions about your background
- **Job Matching Analysis**: Analyze how well you match with specific job descriptions
- **Interactive Web Interface**: Modern, responsive design for optimal user experience

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd career-digital-twin