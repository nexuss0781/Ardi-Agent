import os

# This file contains helper utilities for our agent implementations.

def load_prompt(filename: str) -> str:
    """
    Loads a prompt from the /prompts directory.
    
    Args:
        filename: The name of the markdown file in the /prompts directory.
        
    Returns:
        The content of the prompt file as a string.
        
    Raises:
        FileNotFoundError: If the prompt file cannot be found.
    """
    # Build the absolute path to the prompts directory
    # os.path.dirname(__file__) gets the directory of the current file (e.g., /backend/agents)
    prompt_path = os.path.join(os.path.dirname(__file__), '..', '..', 'prompts', filename)
    
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")
        
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()
        
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Add this new function to the file

def create_agent(llm, system_prompt: str, tools: List[BaseTool]) -> AgentExecutor:
    """
    A factory function to create a LangChain agent executor.
    
    Args:
        llm: The language model instance to be used.
        system_prompt: The system prompt or "constitution" for the agent.
        tools: A list of tools the agent is allowed to use.
        
    Returns:
        A runnable AgentExecutor instance.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)