from typing import Dict, Any
import litellm

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt

class AdjudicationUnit(GroupSupervisor):
    """
    The supervisor for the Adjudication Unit (The Justifier).
    This agent is now intelligent and makes binding rulings on disputes.
    """
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Overrides the stub method to implement the dispute resolution logic.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")
        
        # 1. Load the specific prompt for the Justifier
        system_prompt = load_prompt("justifier.md")
        
        # 2. Prepare the input dossier for the Justifier
        review_dossier = state.get("review_dossier", {})
        input_content = (
            f"A dispute has been raised. Here is the dossier:\n\n"
            f"--- START DOSSIER ---\n"
            f"PLAN UNDER REVIEW:\n{review_dossier.get('plan_reviewed', 'N/A')}\n\n"
            f"QA COUNCIL FEEDBACK:\n{review_dossier.get('feedback', 'N/A')}\n\n"
            f"SUPERVISOR'S REASON FOR DISPUTE:\n{review_dossier.get('dispute_reason', 'No reason provided.')}\n"
            f"--- END DOSSIER ---\n\n"
            f"Based on this information, you must make a final, binding decision. "
            f"Your output must be a single word: UPHOLD or OVERRULE."
        )

        # 3. Use the Leader model to make the final decision
        try:
            response = litellm.completion(
                model=self.leader_model.get("unique_name"),
                messages=[{
                    "role": "system", 
                    "content": system_prompt
                }, {
                    "role": "user",
                    "content": input_content
                }],
                temperature=0.0
            )
            
            ruling = response.choices[0].message.content.strip().upper()
            # Ensure the output is ONLY one of the two valid words
            if ruling not in ["UPHOLD", "OVERRULE"]:
                ruling = "OVERRULE" # Default to overruling if output is invalid
            
        except Exception as e:
            print(f"--- [Agent] CRITICAL ERROR in {self.group_name}: {e} ---")
            ruling = "ERROR"

        # 4. Return the updates for the master state
        return {
            "history_log": state.get("history_log", []) + [f"The {self.group_name} has made a ruling: {ruling}."],
            "dispute_ruling": ruling,
            "dispute_raised": False # Reset the dispute flag
        }