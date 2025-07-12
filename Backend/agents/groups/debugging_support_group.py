from typing import Dict, Any
from langchain_groq import ChatGroq

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt, create_agent
from tools.agent_tools import read_file, write_file, list_files, execute_in_sandbox

class DebuggingSupportGroup(GroupSupervisor):
    """
    The supervisor for the Debugging & Support Group.
    This agent is now active and uses tools to fix code based on QA feedback.
    """
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Activates the debugging agent to fix code based on QA feedback.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")
        
        review_dossier = state.get("review_dossier", {})
        qa_feedback = review_dossier.get("feedback", "No feedback provided.")

        print(f"    - Task: Fixing code based on QA feedback.")

        # 1. Initialize LLM and tools
        llm = ChatGroq(temperature=0.0, model_name=self.leader_model.get("unique_name"))
        system_prompt = load_prompt("debugger.md")
        tools = [read_file, write_file, list_files, execute_in_sandbox]

        # 2. Create the agent executor
        agent_executor = create_agent(llm, system_prompt, tools)
        
        # 3. Prepare the input for the agent
        input_content = (
            f"The code has failed the Quality Assurance check. Your task is to fix it.\n\n"
            f"Here is the feedback from the QA Council:\n--- QA FEEDBACK ---\n{qa_feedback}\n--- END QA FEEDBACK ---\n\n"
            f"Please analyze the feedback, read the relevant files, fix the bug, and then verify your fix by re-running the tests."
        )

        # 4. Invoke the agent to perform the debugging task
        try:
            response = agent_executor.invoke({"input": input_content})
            fix_summary = response['output']
            
        except Exception as e:
            print(f"--- [Agent] CRITICAL ERROR during debugging: {e} ---")
            fix_summary = f"Error attempting to debug code: {e}"

        return {
            "history_log": state.get("history_log", []) + [f"{self.group_name} attempted a fix: {fix_summary}"],
            # Clear the review dossier as the code has been changed
            "review_dossier": None 
        }