# backend/agent/core.py
import os
from typing import Dict, Any, List, Annotated
from datetime import datetime
import json

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool

# Define our state
class AgentState(Dict[str, Any]):
    messages: List[Dict[str, Any]]
    current_page_content: str = ""
    browser_context: Dict[str, Any] = {}
    user_preferences: Dict[str, Any] = {}

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0.1,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define tools for the agent
def search_web(query: str) -> str:
    """Search the web for current information"""
    search = DuckDuckGoSearchRun()
    return search.run(query)

def analyze_current_page(content: str) -> str:
    """Analyze the current webpage content"""
    # This will be enhanced with actual browser integration
    return f"Analyzed page content: {content[:500]}..."

def extract_page_info(selector: str) -> str:
    """Extract specific information from the current page"""
    return f"Extracted information using selector: {selector}"

def summarize_content(content: str) -> str:
    """Summarize the given content"""
    return llm.invoke(f"Please summarize this content: {content}").content

# Create tools
tools = [
    Tool(
        name="web_search",
        func=search_web,
        description="Search the web for current information"
    ),
    Tool(
        name="analyze_page",
        func=analyze_current_page,
        description="Analyze the current webpage content"
    ),
    Tool(
        name="extract_info",
        func=extract_page_info,
        description="Extract specific information from the current page"
    ),
    Tool(
        name="summarize",
        func=summarize_content,
        description="Summarize content or web pages"
    )
]

# Create the ReAct agent
agent = create_react_agent(llm, tools)

# Define the graph workflow
def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the agent wants to use a tool, continue
    if hasattr(last_message, 'tool_calls') and len(last_message.tool_calls) > 0:
        return "continue"
    
    # If it's a final answer, end
    return "end"

def call_agent(state: AgentState):
    messages = state["messages"]
    response = agent.invoke({"messages": messages})
    return {"messages": [response["messages"][-1]]}

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_agent)
workflow.add_node("tools", agent)

# Add edges
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")

# Compile the graph
graph = workflow.compile()