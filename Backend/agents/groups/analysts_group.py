from typing import Dict, Any
from langchain_groq import ChatGroq

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt, create_agent
from tools.agent_tools import (
    advanced_web_search, 
    write_file, 
    read_file, 
    list_files, 
    generate_mermaid_syntax
)

class AnalystsGroup(GroupSupervisor):
    """
    The supervisor for the Research & Architecture Group (Analysts).
    This agent is now intelligent and uses multiple tools to create
    a detailed technical plan and test cases.
    """
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Overrides the stub method to implement the intelligent agent logic.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")
        
        # 1. Initialize the LLM for the Leader model
        # We use zero temperature for precision and adherence to format.
        llm = ChatGroq(
            temperature=0.0, 
            model_name=self.leader_model.get("unique_name")
        )
        
        # 2. Load the prompt and define the tools for the Analyst
        system_prompt = load_prompt("analyst.md")
        tools = [
            advanced_web_search, 
            read_file, 
            list_files, 
            generate_mermaid_syntax
        ]
        
        # 3. Create the agent executor
        agent_executor = create_agent(llm, system_prompt, tools)
        
        # 4. Prepare the input from the state
        # The Analyst needs the conceptual plan to create the technical plan.
        input_content = (
            f"Please create a detailed Technical Plan based on the following "
            f"Conceptual Plan, which can be found at 'conceptual_plan.md'. "
            f"Make sure to include a technology stack, file structure, "
            f"API endpoints if necessary, and a comprehensive set of "
            f"acceptance and unit test cases. Also, create a system "
            f"architecture diagram.\n\n"
            f"Here is the content of the conceptual plan for your convenience:\n---"
            f"\n{state['conceptual_plan']}\n---"
        )
        
        # 5. Invoke the agent to generate the Technical Plan and Test Cases
        try:
            response = agent_executor.invoke({"input": input_content})
            technical_plan_and_tests = response['output']
            
            # 6. Save the generated plan to the workspace
            print("--- [Agent] Saving Technical Plan to workspace... ---")
            write_file(
                path="technical_plan.md", 
                content=technical_plan_and_tests
            )
            
        except Exception as e:
            print(f"--- [Agent] CRITICAL ERROR in {self.group_name}: {e} ---")
            technical_plan_and_tests = f"Error: Could not generate Technical Plan. Details: {e}"

        # 7. Return the updates for the master state
        # For simplicity, we store the whole document. In a real system, we might
        # parse the test cases into a separate state field.
        return {
            "history_log": state.get("history_log", []) + [f"{self.group_name} created the Technical Plan and Test Cases."],
            "technical_plan": technical_plan_and_tests,
            "test_cases": "Test cases are included within the technical_plan.md document." # Placeholder
        }