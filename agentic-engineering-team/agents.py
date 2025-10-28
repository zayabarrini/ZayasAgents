from crewai import Agent
from tools.docker_tools import DockerTools
from tools.code_tools import CodeTools
from tools.testing_tools import TestingTools

def create_agents():
    """Create and return the 4-agent engineering team"""
    
    # Project Manager Agent
    project_manager = Agent(
        role="Senior Project Manager",
        goal="Oversee the entire software development lifecycle and ensure project success",
        backstory="""You are an experienced project manager with 10+ years in software development.
        You excel at requirement analysis, project planning, and team coordination. You ensure
        that projects are delivered on time and meet all specifications.""",
        tools=[],
        verbose=True,
        allow_delegation=True
    )
    
    # Software Architect Agent
    software_architect = Agent(
        role="Software Architect",
        goal="Design robust and scalable software architecture",
        backstory="""You are a senior software architect specializing in designing clean,
        maintainable, and scalable systems. You have expertise in multiple programming
        languages and frameworks, with a focus on best practices and design patterns.""",
        tools=[CodeTools.analyze_requirements, CodeTools.design_architecture],
        verbose=True,
        allow_delegation=True
    )
    
    # Senior Developer Agent
    senior_developer = Agent(
        role="Senior Full-Stack Developer",
        goal="Write high-quality, efficient, and maintainable code",
        backstory="""You are a senior developer with expertise in multiple programming languages
        and frameworks. You write clean, tested, and efficient code following best practices.
        You're proficient in both frontend and backend development.""",
        tools=[CodeTools.write_code, CodeTools.review_code, DockerTools.create_dockerfile],
        verbose=True,
        allow_delegation=False
    )
    
    # QA Engineer Agent
    qa_engineer = Agent(
        role="Quality Assurance Engineer",
        goal="Ensure software quality through comprehensive testing",
        backstory="""You are a meticulous QA engineer with expertise in automated testing,
        manual testing, and CI/CD pipelines. You ensure that all code meets quality standards
        and is thoroughly tested before deployment.""",
        tools=[TestingTools.write_tests, TestingTools.run_tests, DockerTools.build_image, DockerTools.run_container],
        verbose=True,
        allow_delegation=False
    )
    
    return {
        'project_manager': project_manager,
        'software_architect': software_architect,
        'senior_developer': senior_developer,
        'qa_engineer': qa_engineer
    }