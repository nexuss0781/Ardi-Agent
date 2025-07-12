import os
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from backend.state import AgentState
from tools.agent_tools import advanced_web_search, write_file, read_file
from tools.user_tools import ask_user_confirmation

# --- Agent Configuration ---

# Initialize the LLM we will use for our agents.
# We use Groq for its speed, which is excellent for agentic workflows.
# Temperature is set to 0 to encourage deterministic, predictable outputs.
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")

# --- Tool Definitions for LangChain ---
# We wrap our existing functions in the @tool decorator for LangChain compatibility.
@tool
def web_search_tool(query: str) -> str:
    """Performs a web search to find information."""
    return advanced_web_search(query)

@tool
def write_file_tool(path: str, content: str) -> str:
    """Writes content to a file in the workspace."""
    return write_file(path, content)

@tool
def read_file_tool(path: str) -> str:
    """Reads content from a file in the workspace."""
    return read_file(path)

# --- Prompt Loading ---
def load_prompt(filename: str) -> str:
    """Loads a prompt from the /prompts directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(prompt_path, 'r') as f:
        return f.read()

# --- Helper Function to Create Agents ---
def create_agent(system_prompt: str, tools: List):
    """Factory function to create a LangChain agent."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Intelligent Worker Nodes ---

def initial_user_interaction_node(state: AgentState) -> Dict[str, Any]:
    """

    The first intelligent node. It refines the user's query.
    """
    print("--- [Agent] Executing: Language Expert ---")
    system_prompt = load_prompt("language_expert.md")
    # This agent needs no tools, it just performs a transformation.
    agent_executor = create_agent(system_prompt, [])
    
    refined_query = agent_executor.invoke({
        "input": state['initial_request']
    })['output']
    
    return {
        "refined_query": refined_query,
        "last_completed_step": "initial_user_interaction_node"
    }

def idea_generators_node(state: AgentState) -> Dict[str, Any]:
    """
    Generates the conceptual plan.
    """
    print("--- [Agent] Executing: Idea Generator ---")
    system_prompt = load_prompt("idea_generator.md")
    # This agent can use web search for inspiration.
    agent_executor = create_agent(system_prompt, [web_search_tool])
    
    conceptual_plan = agent_executor.invoke({
        "input": state['refined_query']
    })['output']

    # We also save the plan to a file in the workspace
    write_file_tool.invoke({
        "path": "conceptual_plan.md", 
        "content": conceptual_plan
    })
    
    return {
        "conceptual_plan": conceptual_plan,
        "last_completed_step": "idea_generators_node"
    }

def analysts_node(state: AgentState) -> Dict[str, Any]:
    """
    Generates the technical plan.
    """
    print("--- [Agent] Executing: Analyst ---")
    system_prompt = load_prompt("analyst.md")
    # The analyst needs to read the conceptual plan and can use web search.
    tools = [read_file_tool, web_search_tool]
    agent_executor = create_agent(system_prompt, tools)
    
    # The input for this agent is the conceptual plan.
    input_content = f"Here is the Conceptual Plan:\n\n{state['conceptual_plan']}"
    
    technical_plan = agent_executor.invoke({
        "input": input_content
    })['output']

    # We also save the plan to a file in the workspace
    write_file_tool.invoke({
        "path": "technical_plan.md", 
        "content": technical_plan
    })

    return {
        "technical_plan": technical_plan,
        "last_completed_step": "analysts_node"
    }

# --- Stubbed Nodes (To be implemented in later phases) ---

def developers_node(state: AgentState) -> Dict[str, Any]:
    """
    STUB: Simulates the work of the Development team.
    """
    print("--- [STUB] Executing: Developers Node ---")
    files = {
        "src/main.py": "print('Hello, World! I am a stubbed developer.')",
        "README.md": "# Project Readme\nThis project was planned by real agents, but coded by a stub."
    }
    return {
        "files": files,
        "last_completed_step": "developers_node"
    }

def evaluators_node(state: AgentState) -> Dict[str, Any]:
    """
    STUB: Simulates the work of the Evaluators.
    """
    print("--- [STUB] Executing: Evaluators Node ---")
    feedback_history = state.get("feedback_history", [])
    feedback_history.append("Stubbed code review passed.")
    return {
        "feedback_history": feedback_history,
        "last_completed_step": "evaluators_node"
    }

def user_confirmation_node(state: AgentState) -> Dict[str, Any]:
    """
    Uses a tool to pause the workflow and ask for user approval.
    """
    print("--- [Agent] Executing: User Confirmation Node ---")
    user_response = ask_user_confirmation(
        "Plans have been generated in the /workspace directory. Please review them. Do you approve?"
    )
    return {
        "user_feedback": user_response,
        "last_completed_step": "user_confirmation_node"
    }

def project_completion_node(state: AgentState) -> Dict[str, Any]:
    """
    A terminal node.
    """
    print("--- [Agent] Executing: Project Completion Node ---")
    return {
        "last_completed_step": "project_completion_node"
    }