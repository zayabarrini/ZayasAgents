agentic-engineering-team/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── main.py
├── tasks.py
├── agents.py
├── tools/
│   ├── __init__.py
│   ├── docker_tools.py
│   ├── code_tools.py
│   └── testing_tools.py
├── test_app/
│   ├── app.py
│   ├── requirements.txt
│   ├── test_app.py
│   └── Dockerfile
└── README.md

Development workflow commands:

# Initialize project (run once)
chmod +x setup.sh
./setup.sh

# Or on Windows
# .\setup.ps1

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\Activate.ps1  # Windows

# Run linting and formatting
black .
isort .
flake8 .
mypy .

# Run tests
pytest test_app/ -v

# Run pre-commit on all files
pre-commit run --all-files

# Run the application
python main.py

# Run with Docker
docker-compose up --build



# Agentic AI Engineering Team

A 4-agent CrewAI system that manages, builds, and tests software applications in Docker.

## Agents

1. **Project Manager** - Oversees project lifecycle
2. **Software Architect** - Designs system architecture
3. **Senior Developer** - Implements code
4. **QA Engineer** - Tests and deploys application

## Setup

1. Clone the repository
2. Set up environment variables:
   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env