from typing import Dict, Any
import litellm

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt

class UserEngagementGroup(GroupSupervisor):
    """
    The supervisor for the User Engagement Group.
    This agent is now intelligent and handles dialogue and brief creation.
    """
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Overrides the stub method to implement intelligent agent logic.
        
        For its first task, it will generate clarifying questions based on
        the user's refined query.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")
        
        # Determine the task. For now, we assume it's to generate questions.
        # In a more complex flow, we might check the last_completed_step.
        
        print(f"    - Task: Generating clarifying questions...")
        
        # 1. Load the specific prompt for this task
        system_prompt_template = load_prompt("user_engagement.md")
        
        # 2. Prepare the input for the LLM
        input_content = f"The user's refined project query is: '{state['refined_query']}'"
        
        # 3. Create the LLM instance for the Leader model and get the questions
        try:
            response = litellm.completion(
                model=self.leader_model.get("unique_name"),
                messages=[{
                    "role": "system",
                    "content": system_prompt_template
                }, {
                    "role": "user",
                    "content": input_content
                }],
                temperature=0.1 # A little creativity is okay for questions
            )
            
            generated_questions = response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"--- [Agent] CRITICAL ERROR in {self.group_name}: {e} ---")
            generated_questions = "Error: Could not generate clarifying questions."

        # 4. Return the updates to be merged into the master state
        return {
            "history_log": state.get("history_log", []) + [f"{self.group_name} generated clarifying questions for the user."],
            "clarification_questions": generated_questions
        }