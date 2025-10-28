# agent_creator.py
import autogen
import json
import os
from typing import Dict, List, Any
import yaml

class AgentCreator:
    """
    An AI agent that can design, build, and launch new specialized agents using AutoGen.
    """
    
    def __init__(self, config_path: str = "config.json"):
        self.config_list = autogen.config_list_from_json(
            config_path,
            filter_dict={
                "model": ["gpt-4", "gpt-4-32k", "gpt-4-turbo-preview"]
            }
        )
        self.llm_config = {"config_list": self.config_list}
        self.agent_registry = {}
        self.load_existing_agents()
        
        # Initialize the master creator agent
        self.creator_agent = autogen.AssistantAgent(
            name="AgentCreator",
            system_message="""
            You are an expert AI Agent Architect. Your role is to design, build, and deploy 
            specialized AI agents using AutoGen. You can:
            
            1. Analyze requirements for new agents
            2. Design agent architectures and capabilities
            3. Generate code for specialized agents
            4. Test and validate agent functionality
            5. Deploy agents to handle specific tasks
            
            You have access to tools that can create, configure, and launch new agents.
            Always think step by step and ensure the agents you create are robust and effective.
            """,
            llm_config=self.llm_config
        )
        
        # User proxy for interaction
        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=10,
            code_execution_config={"work_dir": "agents", "use_docker": False},
            system_message="Human administrator overseeing agent creation process."
        )
    
    def load_existing_agents(self):
        """Load previously created agents from registry"""
        try:
            with open("agent_registry.json", "r") as f:
                self.agent_registry = json.load(f)
        except FileNotFoundError:
            self.agent_registry = {}
    
    def save_agent_registry(self):
        """Save agent registry to file"""
        with open("agent_registry.json", "w") as f:
            json.dump(self.agent_registry, f, indent=2)
    
    def design_agent_specification(self, requirements: str) -> Dict[str, Any]:
        """
        Design a specification for a new agent based on requirements
        """
        designer = autogen.AssistantAgent(
            name="AgentDesigner",
            system_message="""
            You specialize in designing AI agent specifications. Given requirements,
            create a detailed specification including:
            - Agent name and purpose
            - Required capabilities
            - System message template
            - Tools and functions needed
            - Interaction patterns
            - Success criteria
            
            Return your specification as a JSON object.
            """,
            llm_config=self.llm_config
        )
        
        response = designer.generate_reply(
            messages=[{"role": "user", "content": f"Design an agent specification for: {requirements}"}]
        )
        
        # Parse the response to extract specification
        # This is a simplified version - in practice, you'd want more robust parsing
        try:
            spec = json.loads(response)
        except:
            # If JSON parsing fails, create a basic spec
            spec = {
                "name": requirements.replace(" ", "_").lower() + "_agent",
                "purpose": requirements,
                "capabilities": ["reasoning", "code_execution", "tool_usage"],
                "system_message": f"Specialized agent for: {requirements}"
            }
        
        return spec
    
    def generate_agent_code(self, specification: Dict[str, Any]) -> str:
        """
        Generate the Python code for a new agent based on specification
        """
        coder = autogen.AssistantAgent(
            name="AgentCoder",
            system_message="""
            You are an expert Python and AutoGen developer. Given an agent specification,
            generate complete Python code for the agent including:
            - Proper class structure
            - AutoGen agent configuration
            - Required tools and functions
            - Error handling
            - Documentation
            
            Return only the Python code without explanations.
            """,
            llm_config=self.llm_config
        )
        
        response = coder.generate_reply(
            messages=[{"role": "user", "content": f"Generate Python code for this agent specification: {json.dumps(specification, indent=2)}"}]
        )
        
        return response
    
    def create_specialized_agent(self, agent_type: str, requirements: str) -> Dict[str, Any]:
        """
        Create a new specialized agent
        """
        print(f"🤖 Creating {agent_type} agent with requirements: {requirements}")
        
        # Design the agent specification
        spec = self.design_agent_specification(requirements)
        agent_name = spec.get("name", f"{agent_type}_agent")
        
        # Generate the agent code
        agent_code = self.generate_agent_code(spec)
        
        # Save the agent code to file
        agent_dir = f"agents/{agent_name}"
        os.makedirs(agent_dir, exist_ok=True)
        
        agent_file = f"{agent_dir}/{agent_name}.py"
        with open(agent_file, "w") as f:
            f.write(agent_code)
        
        # Create a configuration file
        config = {
            "name": agent_name,
            "type": agent_type,
            "specification": spec,
            "code_file": agent_file,
            "status": "created"
        }
        
        # Register the agent
        self.agent_registry[agent_name] = config
        self.save_agent_registry()
        
        print(f"✅ Successfully created agent: {agent_name}")
        return config
    
    def launch_agent(self, agent_name: str, task: str) -> str:
        """
        Launch a created agent to perform a task
        """
        if agent_name not in self.agent_registry:
            return f"❌ Agent {agent_name} not found in registry"
        
        agent_config = self.agent_registry[agent_name]
        
        try:
            # Dynamically import and create the agent
            # Note: In production, you'd want a more robust dynamic import system
            spec = agent_config["specification"]
            
            # Create a simple agent based on the specification
            agent = autogen.AssistantAgent(
                name=agent_name,
                system_message=spec.get("system_message", f"Specialized agent for {spec.get('purpose', 'unknown task')}"),
                llm_config=self.llm_config
            )
            
            # Create a user proxy to interact with the agent
            user_proxy = autogen.UserProxyAgent(
                name=f"{agent_name}_user",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=5,
                code_execution_config=False
            )
            
            # Initiate the conversation
            chat_result = user_proxy.initiate_chat(
                agent,
                message=task
            )
            
            return f"✅ Agent {agent_name} completed task successfully"
            
        except Exception as e:
            return f"❌ Error launching agent {agent_name}: {str(e)}"
    
    def list_agents(self) -> List[str]:
        """List all created agents"""
        return list(self.agent_registry.keys())
    
    def get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        """Get information about a specific agent"""
        return self.agent_registry.get(agent_name, {})
    
    def interactive_creation(self):
        """
        Interactive mode for creating agents through conversation
        """
        print("🎯 Agent Creator Interactive Mode Activated!")
        print("Describe the type of agent you want to create...")
        
        self.user_proxy.initiate_chat(
            self.creator_agent,
            message="""
            I want to create specialized AI agents. Help me design and build agents 
            for various tasks. I'll describe what I need, and you help create the agent.
            
            Please guide me through the process and create the agents I need.
            """
        )

# Example specialized agent templates
class AgentTemplates:
    """Pre-built templates for common agent types"""
    
    @staticmethod
    def create_data_analyzer_agent():
        """Create a data analysis agent"""
        return {
            "name": "data_analyzer",
            "system_message": """
            You are a Data Analysis Expert. You can:
            - Analyze datasets and provide insights
            - Generate statistical summaries
            - Create visualizations
            - Identify patterns and trends
            - Provide data-driven recommendations
            
            You work with pandas, numpy, matplotlib and other data science tools.
            """,
            "capabilities": ["data_analysis", "visualization", "statistics"]
        }
    
    @staticmethod
    def create_content_writer_agent():
        """Create a content writing agent"""
        return {
            "name": "content_writer",
            "system_message": """
            You are a Professional Content Writer. You can:
            - Write engaging articles and blog posts
            - Create marketing copy
            - Edit and improve existing content
            - Adapt tone and style for different audiences
            - Generate creative ideas for content
            
            You excel at creating compelling, well-structured written content.
            """,
            "capabilities": ["writing", "editing", "creativity"]
        }
    
    @staticmethod
    def create_research_assistant_agent():
        """Create a research assistant agent"""
        return {
            "name": "research_assistant",
            "system_message": """
            You are a Research Assistant. You can:
            - Conduct literature reviews
            - Summarize research papers
            - Identify key findings and methodologies
            - Compare and contrast different studies
            - Generate research questions and hypotheses
            
            You are thorough, analytical, and methodical in your research approach.
            """,
            "capabilities": ["research", "summarization", "analysis"]
        }

# Main execution
if __name__ == "__main__":
    # Create the agent creator
    creator = AgentCreator()
    
    print("🚀 Agent Creator System Initialized!")
    print("Available commands:")
    print("1. create_agent - Create a new specialized agent")
    print("2. list_agents - List all created agents")
    print("3. launch_agent - Launch an agent for a task")
    print("4. interactive - Enter interactive mode")
    
    while True:
        command = input("\nEnter command (or 'quit' to exit): ").strip().lower()
        
        if command == "quit":
            break
        elif command == "create_agent":
            agent_type = input("Enter agent type: ")
            requirements = input("Enter agent requirements: ")
            creator.create_specialized_agent(agent_type, requirements)
        elif command == "list_agents":
            agents = creator.list_agents()
            print("Created agents:", agents)
        elif command == "launch_agent":
            agent_name = input("Enter agent name: ")
            task = input("Enter task: ")
            result = creator.launch_agent(agent_name, task)
            print(result)
        elif command == "interactive":
            creator.interactive_creation()
        else:
            print("Unknown command")