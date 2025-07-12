import json
import litellm
from typing import Dict, Any
from backend.state import AgentState
from backend.config import GROQ_API_KEY # Import the configured API key

# Configure litellm to use the Groq API key
litellm.api_key = GROQ_API_KEY

# --- The Router's "Constitution" ---
# This prompt is the core instruction set for our routing LLM.
# It strictly defines its role, inputs, and expected output format.
ROUTER_SYSTEM_PROMPT = """
You are the central intelligent router for an AI developer agent. Your one and only job is to decide which worker node to send the project to next.

You will be given the current state of the project as a JSON object. The most important field is "last_completed_step", which tells you what just happened.

Based on the project state, you must return ONLY the name of the next node to execute. Your response must be a single, valid node name and nothing else.

Here are the valid nodes and their purpose:
- "initial_user_interaction_node": Call this first to clarify the user's request.
- "idea_generators_node": Call this after initial interaction to brainstorm features.
- "analysts_node": Call this after brainstorming to create a technical plan.
- "developers_node": Call this when a plan is ready, to write or modify code.
- "evaluators_node": Call this after code is written, to perform tests and QA.
- "user_confirmation_node": Call this when user approval is needed for a plan or a final product.
- "project_completion_node": Call this only when the project is finished and delivered.

Example:
If last_completed_step is "analysts_node", the technical plan is ready. The next logical step is to write code.
Your response must be:
developers_node
"""

def route(state: AgentState) -> str:
    """
    Analyzes the current AgentState and decides which node to call next.
    
    Args:
        state: The current state of the project.
        
    Returns:
        The name of the next node to execute.
    """
    print("--- [Router] Analyzing state to decide next step... ---")
    
    # Prepare the input for the LLM router
    router_input = json.dumps(state, indent=2)
    
    print(f"--- [Router] Current State:\n{router_input}\n---")
    
    # --- Live LLM Call ---
    # The MOCKED LOGIC has been removed. This is now a real call to an LLM.
    try:
        response = litellm.completion(
            model="groq/llama3-8b-8192", # Using a fast model for routing decisions
            messages=[
                {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
                {"role": "user", "content": router_input},
            ],
            temperature=0.0, # We want deterministic routing
            max_tokens=50,
        )
        
        decision = response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"--- [Router] CRITICAL ERROR: Could not get decision from LLM. Error: {e} ---")
        # Fallback to a safe default in case of API failure
        decision = "project_completion_node"

    print(f"--- [Router] Decision: --> {decision} ---")
    
    return decision