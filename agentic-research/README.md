agentic-research/
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── research_agents.py
│   │   └── orchestrator.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── logger.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_orchestrator.py
├── data/
│   ├── sources/
│   └── reports/
├── docs/
├── scripts/
│   ├── setup.sh
│   └── run_research.py
├── logs/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py
└── config.py


# Navigate to project
cd agentic-research

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install