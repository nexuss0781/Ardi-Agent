from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
import litellm

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt # We will create this helper function next

class LanguageExpertGroup(GroupSupervisor):
    """
    The supervisor for the Language Expert Group.
    This agent is now intelligent and uses its Leader model to refine queries.
    """
    
    def __init__(self, group_details: dict):
        # The __init__ from the parent class is sufficient.
        # It already stores the leader model name and other details.
        super().__init__(group_details)
        
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Overrides the stub method to implement intelligent agent logic.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")
        
        # 1. Load the specific prompt for this agent
        system_prompt_template = load_prompt("language_expert.md")
        
        # 2. Create the LLM instance for the Leader model
        # We use litellm.completion and pass the model alias from our taxonomy.
        # This is a simplified approach for agents that don't need complex tools.
        try:
            response = litellm.completion(
                model=self.leader_model.get("unique_name"),
                messages=[{
                    "role": "system",
                    "content": system_prompt_template
                }, {
                    "role": "user",
                    "content": state['initial_request']
                }],
                temperature=0.0
            )
            
            refined_query = response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"--- [Agent] CRITICAL ERROR in {self.group_name}: {e} ---")
            # Fallback to just using the initial request if the LLM fails
            refined_query = f"Error refining query. Using original: {state['initial_request']}"

        # 3. Return the updates to be merged into the master state
        return {
            "history_log": state.get("history_log", []) + [f"{self.group_name} refined the user's query."],
            "refined_query": refined_query
        }