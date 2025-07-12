from typing import Dict, Any
from langchain_groq import ChatGroq

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt, create_agent
from tools.agent_tools import advanced_web_search, write_file

class InnovatorsGroup(GroupSupervisor):
    """
    The supervisor for the Creative & Ideation Group (Innovators).
    This agent is now intelligent and uses tools to generate a Conceptual Plan.
    """
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Overrides the stub method to implement the intelligent agent logic.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")
        
        # 1. Initialize the LLM for the Leader model
        # We use a low temperature for predictable structure, but not zero for creativity.
        llm = ChatGroq(
            temperature=0.2, 
            model_name=self.leader_model.get("unique_name")
        )
        
        # 2. Load the specific prompt and define the tools
        system_prompt = load_prompt("innovator.md")
        tools = [advanced_web_search]
        
        # 3. Create the agent using our new helper function
        agent_executor = create_agent(llm, system_prompt, tools)
        
        # 4. Prepare the input from the state
        # The Innovator needs context from the previous steps.
        input_content = (
            f"The project brief is as follows:\n---"
            f"\n{state['project_brief']}\n---"
            f"\n\nThe research from the analysts provided this context:"
            f"\n---\n{state.get('research_document', 'No research document provided.')}"
        )
        
        # 5. Invoke the agent to generate the Conceptual Plan
        try:
            response = agent_executor.invoke({"input": input_content})
            conceptual_plan = response['output']
            
            # 6. Save the generated plan to the workspace
            print("--- [Agent] Saving Conceptual Plan to workspace... ---")
            write_file(
                path="conceptual_plan.md", 
                content=conceptual_plan
            )
            
        except Exception as e:
            print(f"--- [Agent] CRITICAL ERROR in {self.group_name}: {e} ---")
            conceptual_plan = f"Error: Could not generate Conceptual Plan. Details: {e}"

        # 7. Return the updates for the master state
        return {
            "history_log": state.get("history_log", []) + [f"{self.group_name} created the Conceptual Plan."],
            "conceptual_plan": conceptual_plan
        }