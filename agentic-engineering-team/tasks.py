from crewai import Task

def create_tasks(agents):
    """Create and return tasks for the engineering team"""
    
    # Task 1: Analyze Requirements
    analyze_requirements = Task(
        description="""Analyze the project requirements and create a detailed project plan.
        Requirements: {requirements}
        
        Output should include:
        1. Clear understanding of requirements
        2. Technology stack recommendations
        3. Project timeline estimates
        4. Potential risks and mitigation strategies""",
        agent=agents['project_manager'],
        expected_output="Comprehensive project analysis document with timeline and tech stack"
    )
    
    # Task 2: Design Architecture
    design_architecture = Task(
        description="""Based on the requirements analysis, design the software architecture.
        Create system design, database schema (if needed), and API specifications.
        
        Consider:
        - Scalability
        - Maintainability
        - Security
        - Performance""",
        agent=agents['software_architect'],
        expected_output="Detailed architecture design document with diagrams and specifications",
        context=[analyze_requirements]
    )
    
    # Task 3: Implement Code
    implement_code = Task(
        description="""Implement the application based on the architecture design.
        Write clean, efficient, and well-documented code.
        
        Deliverables:
        - Complete source code
        - Dockerfile for containerization
        - Requirements file
        - Basic documentation""",
        agent=agents['senior_developer'],
        expected_output="Fully functional application code with Docker configuration",
        context=[design_architecture]
    )
    
    # Task 4: Test Application
    test_application = Task(
        description="""Create and execute comprehensive tests for the application.
        Include unit tests, integration tests, and end-to-end tests if applicable.
        
        Deliverables:
        - Test suites
        - Test reports
        - Code coverage analysis
        - Bug reports if any""",
        agent=agents['qa_engineer'],
        expected_output="Test results and quality assurance report",
        context=[implement_code]
    )
    
    # Task 5: Deploy Application
    deploy_application = Task(
        description="""Containerize and deploy the application using Docker.
        Build Docker image, run container, and verify deployment.
        
        Steps:
        1. Build Docker image
        2. Run container
        3. Test deployed application
        4. Generate deployment report""",
        agent=agents['qa_engineer'],
        expected_output="Successfully deployed application with verification tests",
        context=[test_application]
    )
    
    return {
        'analyze_requirements': analyze_requirements,
        'design_architecture': design_architecture,
        'implement_code': implement_code,
        'test_application': test_application,
        'deploy_application': deploy_application
    }