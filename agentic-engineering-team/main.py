import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks

# Load environment variables
load_dotenv()

class EngineeringTeam:
    def __init__(self):
        self.agents = create_agents()
        self.tasks = create_tasks(self.agents)
        
    def run_project(self, project_requirements):
        """Run the engineering team with project requirements"""
        print("🚀 Starting 4-Agent Engineering Team...")
        print(f"📋 Project Requirements: {project_requirements}")
        
        # Set up crew
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=[
                self.tasks['analyze_requirements'],
                self.tasks['design_architecture'],
                self.tasks['implement_code'],
                self.tasks['test_application'],
                self.tasks['deploy_application']
            ],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff(inputs={'requirements': project_requirements})
        return result

def main():
    # Sample project requirements
    project_requirements = """
    Create a simple Flask web application that:
    1. Has a home page showing "Hello from Agentic Engineering Team!"
    2. Includes an API endpoint /api/health that returns JSON status
    3. Has proper error handling
    4. Includes unit tests
    5. Can be containerized with Docker
    """
    
    team = EngineeringTeam()
    result = team.run_project(project_requirements)
    
    print("\n" + "="*50)
    print("🎯 PROJECT COMPLETED!")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()