import json
import litellm
from typing import Dict, Any
from backend.state import AgentState
from backend.taxonomy_registry import taxonomy_registry
from .utils import load_prompt

# Import all agent group classes
from backend.agents.groups.user_engagement_group import UserEngagementGroup
from backend.agents.groups.language_expert_group import LanguageExpertGroup
from backend.agents.groups.analysts_group import AnalystsGroup
from backend.agents.groups.innovators_group import InnovatorsGroup
from backend.agents.groups.frontend_development_group import FrontendDevelopmentGroup
from backend.agents.groups.backend_development_group import BackendDevelopmentGroup
from backend.agents.groups.debugging_support_group import DebuggingSupportGroup
from backend.agents.groups.qa_council import QACouncil
from backend.agents.groups.adjudication_unit import AdjudicationUnit
# We will create a one-off "specialist" for this purpose.
from ..utils import create_agent
from ..agents.utils import load_prompt
from tools.agent_tools import list_files, read_file, write_file
from langchain_groq import ChatGroq

# Add the new import at the top of the file
from tools.notification_tool import send_completion_notification
# This mapping connects a group name from our taxonomy to its actual Python class.
AGENT_CLASS_MAP = {
    "user_engagement_group": UserEngagementGroup,
    "language_expert_group": LanguageExpertGroup,
    "analysts_group": AnalystsGroup,
    "innovators_group": InnovatorsGroup,
    "frontend_development_group": FrontendDevelopmentGroup,
    "backend_development_group": BackendDevelopmentGroup,
    "debugging_support_group": DebuggingSupportGroup,
    "qa_council": QACouncil,
    "adjudication_unit": AdjudicationUnit,
}

def _create_and_execute_agent(group_name: str, state: AgentState) -> Dict[str, Any]:
    """Helper function to instantiate and execute a supervisor stub."""
    group_details = taxonomy_registry.get_group_details(group_name)
    if not group_details:
        raise ValueError(f"No details found for group: {group_name} in the taxonomy registry.")
    
    agent_class = AGENT_CLASS_MAP.get(group_name)
    if not agent_class:
        raise ValueError(f"No agent class found for group: {group_name} in the AGENT_CLASS_MAP.")
        
    supervisor = agent_class(group_details)
    return supervisor.execute(state)

# --- Node Definitions for each of the 17+ Workflow Steps ---

def step_1_initial_request(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 1: Initial Request Received ---")
    return {"history_log": state.get("history_log", []) + ["Step 1: Initial Request Received."], "last_completed_step": "step_1_initial_request"}

def step_2_polish_query(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 2: Polish Query ---")
    updates = _create_and_execute_agent("language_expert_group", state)
    updates["last_completed_step"] = "step_2_polish_query"
    return updates
    
def step_3_user_confirmation_1(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 3: User Confirmation 1 ---")
    return {"history_log": state.get("history_log", []) + ["Step 3: User confirmed refined query (simulated)."], "last_completed_step": "step_3_user_confirmation_1"}

def step_4_deep_clarification(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 4: Deep Clarification ---")
    updates = _create_and_execute_agent("user_engagement_group", state)
    updates["last_completed_step"] = "step_4_deep_clarification"
    return updates

def step_5_final_project_brief(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 5: Final Project Brief & Confirmation 2 ---")
    return {"project_brief": {"summary": "Stubbed project brief."}, "history_log": state.get("history_log", []) + ["Step 5: Project Brief created and confirmed (simulated)."], "last_completed_step": "step_5_final_project_brief"}

def step_6_market_analysis(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 6: Market & Feature Analysis ---")
    updates = _create_and_execute_agent("analysts_group", state)
    updates["last_completed_step"] = "step_6_market_analysis"
    return updates

def step_7_creative_ideation(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 7: Creative Ideation ---")
    updates = _create_and_execute_agent("innovators_group", state)
    updates["last_completed_step"] = "step_7_creative_ideation"
    return updates

def step_8_internal_review_1(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 8: Internal Review of Conceptual Plan ---")
    updates = _create_and_execute_agent("qa_council", state)
    updates["dispute_raised"] = False
    updates["last_completed_step"] = "step_8_internal_review_1"
    return updates

def step_9_technical_planning(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 9: Technical Implementation & Test Case Planning ---")
    updates = _create_and_execute_agent("analysts_group", state)
    updates["last_completed_step"] = "step_9_technical_planning"
    return updates

def step_10_internal_review_2(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 10: Internal Review of Technical Plan ---")
    updates = _create_and_execute_agent("qa_council", state)
    updates["dispute_raised"] = False
    updates["last_completed_step"] = "step_10_internal_review_2"
    return updates

def step_11_present_plan_to_user(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 11: Present Full Plan to User ---")
    return {"history_log": state.get("history_log", []) + ["Step 11: Full plan presented to user (simulated)."], "last_completed_step": "step_11_present_plan_to_user"}

def step_12_user_feedback_loop(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 12: Main User Feedback Loop ---")
    return {"user_feedback": "approve", "history_log": state.get("history_log", []) + ["Step 12: User approved plan (simulated)."], "last_completed_step": "step_12_user_feedback_loop"}

def step_12a_decompose_plan(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 12a: Decompose Plan into Tasks ---")
    system_prompt_template = load_prompt("task_decomposer.md")
    technical_plan = state.get("technical_plan", "No technical plan found.")
    try:
        response = litellm.completion(model="analyst-pro", messages=[{"role": "system", "content": system_prompt_template}, {"role": "user", "content": technical_plan}], response_format={"type": "json_object"}, temperature=0.0)
        task_list = json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"--- [Node] CRITICAL ERROR in Task Decomposition: {e} ---")
        task_list = [{"id": "error", "description": f"Failed to parse plan: {e}", "group": "debugger", "dependencies": []}]
    return {"history_log": state.get("history_log", []) + ["Step 12a: Decomposed plan into tasks."], "task_list": task_list, "last_completed_step": "step_12a_decompose_plan"}

def step_13_task_execution(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 13: Task Execution ---")
    updates = _create_and_execute_agent("backend_development_group", state)
    updates["last_completed_step"] = "step_13_task_execution"
    return updates

def step_14_qa_loop(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 14: Continuous Quality Assurance Loop ---")
    updates = _create_and_execute_agent("qa_council", state)
    updates["dispute_raised"] = False
    updates["last_completed_step"] = "step_14_qa_loop"
    return updates
# The agent we will use for this task doesn't have a dedicated group in the taxonomy.

def step_15_project_completion(state: AgentState) -> Dict[str, Any]:
    """
    Node for Step 15: This node now intelligently generates a README.md
    and sends a completion notification.
    """
    print("--- [Node] Executing Step 15: Project Completion & Professional Packaging ---")
    
    # --- Generate README ---
    readme_agent_llm = ChatGroq(temperature=0.1, model_name="analyst-pro")
    readme_prompt = load_prompt("readme_generator.md")
    readme_tools = [list_files, read_file]
    readme_agent = create_agent(readme_agent_llm, readme_prompt, readme_tools)
    
    try:
        print("--- [Agent] Generating README.md... ---")
        readme_content = readme_agent.invoke({"input": "Analyze the workspace and generate a README.md."})['output']
        write_file("README.md", readme_content)
        readme_status = "README.md generated successfully."
    except Exception as e:
        readme_status = f"Error generating README: {e}"
        print(f"--- [Node] ERROR during README generation: {e} ---")

    # --- Send Notification ---
    summary = state.get("project_brief", {}).get("summary", state.get("initial_request", "N/A"))
    run_id_for_log = state.get('initial_request', 'unknown')[:20] # a pseudo run_id
    notification_status = send_completion_notification(
        project_summary=summary, 
        run_id=run_id_for_log
    )
    
    history_log_entry = f"Step 15: Project packaged. README status: [{readme_status}]. Notification status: [{notification_status}]."

    return {
        "history_log": state.get("history_log", []) + [history_log_entry],
        "last_completed_step": "step_15_project_completion"
    }
def step_16_post_delivery_review(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Step 16: Post-Delivery User Review ---")
    return {"user_feedback": "complete", "history_log": state.get("history_log", []) + ["Step 16: User marked project complete."], "last_completed_step": "step_16_post_delivery_review"}
def step_17_reengage_workflow(state: AgentState) -> Dict[str, Any]:
    """
    This node resets the agent's state for a new request, enabling the
    perpetual partnership loop.
    """
    print("--- [Node] Executing Step 17: Re-Engaging for New Project ---")
    
    # The new user request is stored in the 'user_feedback' field from the previous step
    new_request = state.get("user_feedback", "No new request provided.")
    
    # We create a new, clean initial state, preserving only the new request.
    new_state = {
        "initial_request": new_request,
        "history_log": [f"--- NEW PROJECT STARTED ---", f"Initial Request: {new_request}"],
        # Reset all other fields
        "dispute_raised": False, "refined_query": None, "user_dialogue_history": None, 
        "project_brief": None, "clarification_questions": None, "research_document": None,
        "conceptual_plan": None, "technical_plan": None, "test_cases": None, 
        "task_list": None, "current_task_id": None, "project_files": None, 
        "review_dossier": None, "dispute_ruling": None, "user_feedback": None, 
        "last_completed_step": "step_17_reengage_workflow"
    }
    return new_state

def step_dispute_resolution(state: AgentState) -> Dict[str, Any]:
    print("--- [Node] Executing Dispute Resolution Step ---")
    updates = _create_and_execute_agent("adjudication_unit", state)
    updates["last_completed_step"] = "step_dispute_resolution"
    return updates

### **File Name: `/backend/graph.py` (Fully Corrected & Complete)**