# advanced_agent_creator.py
"""
Advanced features for the Agent Creator system
"""
import autogen
from autogen import GroupChat, GroupChatManager

class AdvancedAgentCreator(AgentCreator):
    """
    Extended Agent Creator with advanced capabilities
    """
    
    def create_multi_agent_system(self, system_spec: Dict[str, Any]) -> List[str]:
        """
        Create a coordinated multi-agent system
        """
        agents_created = []
        
        for agent_spec in system_spec.get("agents", []):
            agent_config = self.create_specialized_agent(
                agent_spec["type"],
                agent_spec["requirements"]
            )
            agents_created.append(agent_config["name"])
        
        # Create coordination mechanism
        self._create_coordinator_agent(system_spec, agents_created)
        
        return agents_created
    
    def _create_coordinator_agent(self, system_spec: Dict[str, Any], agent_names: List[str]):
        """Create a coordinator agent for multi-agent systems"""
        coordinator_spec = {
            "name": f"{system_spec['name']}_coordinator",
            "purpose": f"Coordinate the {system_spec['name']} multi-agent system",
            "system_message": f"""
            You are the Coordinator for the {system_spec['name']} system.
            You manage and coordinate between these agents: {', '.join(agent_names)}.
            
            Your responsibilities:
            - Route tasks to appropriate specialized agents
            - Synthesize results from multiple agents
            - Manage workflow and dependencies
            - Ensure overall system coherence
            
            You have access to all specialized agents in the system.
            """,
            "capabilities": ["coordination", "routing", "synthesis"]
        }
        
        return self.create_specialized_agent("coordinator", json.dumps(coordinator_spec))
    
    def create_self_improving_agent(self, base_requirements: str) -> str:
        """
        Create an agent that can improve itself over time
        """
        self_improver_spec = {
            "name": "self_improving_agent",
            "purpose": f"Self-improving agent for: {base_requirements}",
            "system_message": f"""
            You are a Self-Improving AI Agent. Your primary capability is to 
            analyze your own performance and suggest improvements.
            
            Base purpose: {base_requirements}
            
            You can:
            - Analyze your own responses for quality and effectiveness
            - Identify areas for improvement in your reasoning
            - Suggest modifications to your own system message
            - Learn from interactions and adapt your approach
            
            Continuously work to become more effective at your designated tasks.
            """,
            "capabilities": ["self_analysis", "improvement", "adaptation"]
        }
        
        config = self.create_specialized_agent("self_improver", json.dumps(self_improver_spec))
        return config["name"]

# Example: Create a complete business analysis system
def create_business_analysis_system():
    """Create a multi-agent system for business analysis"""
    creator = AdvancedAgentCreator()
    
    system_spec = {
        "name": "business_analytics",
        "agents": [
            {
                "type": "data_collector",
                "requirements": "Collect and preprocess business data from various sources"
            },
            {
                "type": "financial_analyzer", 
                "requirements": "Analyze financial data, calculate metrics, identify trends"
            },
            {
                "type": "market_analyst",
                "requirements": "Analyze market conditions, competition, opportunities"
            },
            {
                "type": "report_generator",
                "requirements": "Synthesize findings into comprehensive business reports"
            }
        ]
    }
    
    agents = creator.create_multi_agent_system(system_spec)
    print(f"✅ Created business analytics system with agents: {agents}")
    return agents