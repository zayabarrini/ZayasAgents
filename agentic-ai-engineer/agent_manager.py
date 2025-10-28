# agent_manager.py
"""
Agent Manager - Manages and monitors created agents
"""
import json
import time
from datetime import datetime

class AgentManager:
    def __init__(self, registry_file="agent_registry.json"):
        self.registry_file = registry_file
        self.performance_log = "agent_performance.log"
    
    def monitor_agent_performance(self):
        """Monitor and log agent performance"""
        with open(self.registry_file, "r") as f:
            registry = json.load(f)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(registry),
            "active_agents": [name for name, config in registry.items() 
                            if config.get("status") == "active"],
            "registry_snapshot": registry
        }
        
        with open(self.performance_log, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_agent_stats(self):
        """Get statistics about created agents"""
        with open(self.registry_file, "r") as f:
            registry = json.load(f)
        
        stats = {
            "total_agents": len(registry),
            "agent_types": {},
            "creation_dates": [],
            "status_count": {}
        }
        
        for agent_name, config in registry.items():
            agent_type = config.get("type", "unknown")
            status = config.get("status", "unknown")
            
            stats["agent_types"][agent_type] = stats["agent_types"].get(agent_type, 0) + 1
            stats["status_count"][status] = stats["status_count"].get(status, 0) + 1
        
        return stats

# Example usage script
def demo_agent_creation():
    """Demonstrate the Agent Creator in action"""
    creator = AgentCreator()
    
    # Create some example agents
    print("🧪 Creating example agents...")
    
    # Data analyzer agent
    creator.create_specialized_agent(
        "data_analyzer",
        "Analyze datasets, create visualizations, provide insights"
    )
    
    # Content writer agent
    creator.create_specialized_agent(
        "content_writer", 
        "Write engaging content, blog posts, marketing copy"
    )
    
    # Research assistant agent
    creator.create_specialized_agent(
        "research_assistant",
        "Conduct research, summarize papers, analyze findings"
    )
    
    # List all created agents
    agents = creator.list_agents()
    print(f"✅ Created agents: {agents}")
    
    # Demonstrate launching an agent
    if agents:
        task = "Analyze this sales data and provide key insights"
        result = creator.launch_agent(agents[0], task)
        print(f"Launch result: {result}")

if __name__ == "__main__":
    demo_agent_creation()