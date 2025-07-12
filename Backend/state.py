from typing import TypedDict, List, Dict, Optional, Any

# This file defines the master state object for our agentic workflow,
# designed to be the single source of truth for the entire 17-step process.

class AgentState(TypedDict):
    """
    The complete, centralized state of the project being worked on.
    This object is passed between all nodes in the LangGraph graph.
    """

    # --- Core Inputs & Brief (Phase 1 Workflow) ---
    initial_request: str
    refined_query: Optional[str]
    user_dialogue_history: Optional[List[Dict[str, str]]]
    project_brief: Optional[Dict[str, Any]]

# ADD THE NEW FIELD to the AgentState TypedDict
# ... (inside the AgentState class)
    # ...
    project_brief: Optional[Dict[str, Any]]
    clarification_questions: Optional[str] # <<< ADD THIS LINE

    # --- Planning & Research Artifacts (Phase 2 Workflow) ---
    # ...

    # --- Planning & Research Artifacts (Phase 2 Workflow) ---
    research_document: Optional[str]
    conceptual_plan: Optional[str]
    technical_plan: Optional[str]
    test_cases: Optional[List[Dict[str, str]]]

    # --- Execution & Code (Phase 4 Workflow) ---
    task_list: Optional[List[Dict]]
    current_task_id: Optional[str]
    project_files: Optional[Dict[str, str]] # Virtual file system: path -> content

    # --- Governance & QA (Steps 8, 10, 14) ---
    # A dictionary holding the artifact being reviewed and the feedback given.
    review_dossier: Optional[Dict[str, Any]] 
    # The final ruling from the Justifier: "UPHOLD" or "OVERRULE".
    dispute_ruling: Optional[str]
    # A flag set by a Supervisor to trigger the Justifier.
    dispute_raised: bool

    # --- User Interaction & Workflow Tracking ---
    user_feedback: Optional[str]
    last_completed_step: Optional[str] # e.g., "step_8_internal_review_1"
    history_log: List[str] # A human-readable log of all actions taken