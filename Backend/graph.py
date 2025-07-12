import json
import litellm
from langgraph.graph import StateGraph, END
from backend.state import AgentState
from backend.graph_nodes import *

# This file assembles our entire agentic workflow and includes the intelligent router.

ROUTER_PROMPT = """
You are an expert project manager and workflow router. Based on the current state of a software project, you must decide the very next step in the workflow.
Your output MUST be a single, valid node name from the provided list. Do not add any other text.

**Project State:**
{state}

**Workflow Analysis:**
- After initial user request (`step_1`), polish the query (`step_2`).
- After polishing (`step_2`), confirm with the user (`step_3`).
- After confirmation (`step_3`), perform deep clarification (`step_4`).
- After clarification (`step_4`), create the final project brief (`step_5`).
- After the brief is created (`step_5`), begin market analysis (`step_6`).
- After market analysis (`step_6`), perform creative ideation (`step_7`).
- After ideation (`step_7`), conduct the first internal review (`step_8`).
- If a plan review (`step_8` or `step_10`) has a `dispute_raised` flag set to True, you MUST route to `step_dispute_resolution`.
- After a successful first review (`step_8`), begin technical planning (`step_9`).
- After technical planning (`step_9`), conduct the second internal review (`step_10`).
- After a successful second review (`step_10`), present the plan to the user (`step_11`).
- After presenting the plan (`step_11`), enter the user feedback loop (`step_12`).
- If user feedback (`step_12`) is not 'approve', loop back to `step_6_market_analysis` to restart planning.
- If user feedback (`step_12`) is 'approve', decompose the plan into tasks (`step_12a`).
- After decomposing the plan (`step_12a`), begin task execution (`step_13`).
- After task execution (`step_13`), run the QA loop (`step_14`).
- After the QA loop (`step_14`), finalize the project (`step_15`).
- After finalization (`step_15`), enter the post-delivery review (`step_16`).
- After post-delivery review (`step_16`), re-engage for new tasks (`step_17`).
- After re-engagement (`step_17`), the workflow ends until a new request is made.

Based on the state, what is the single next node to execute?
"""
def intelligent_router(state: AgentState) -> str:
    """An intelligent router that uses an LLM and hardcoded checks to decide the next step."""
    print("--- [Router] Intellectually analyzing state for next step... ---")
    last_step = state.get("last_completed_step")
    
    # --- Hardcoded Conditional Logic for Critical Loops ---
    
    if last_step in ["step_8_internal_review_1", "step_10_internal_review_2", "step_14_qa_loop"] and state.get("dispute_raised"):
        print("--- [Router] Dispute detected! Routing to Justifier. ---")
        return "step_dispute_resolution"
            
    if last_step == "step_12_user_feedback_loop" and state.get("user_feedback") != "approve":
        print("--- [Router] User requested revisions. Routing back to planning. ---")
        return "step_6_market_analysis"

    # The new, final piece of logic for the perpetual partnership
    if last_step == "step_16_post_delivery_review":
        if state.get("user_feedback") != "complete":
             print("--- [Router] User has a new request! Re-engaging workflow. ---")
             return "step_17_reengage_workflow" # This leads to a reset and start over
        else:
            print("--- [Router] User confirmed project is complete. Ending workflow. ---")
            return END

    # --- LLM-Powered Routing for Standard Progression ---
    state_str = json.dumps(state, indent=2, default=str)
    prompt = ROUTER_PROMPT.format(state=state_str)
    try:
        response = litellm.completion(model="fast-router", messages=[{"role": "user", "content": prompt}], temperature=0.0)
        next_node = response.choices[0].message.content.strip().split('\n')[0]
        print(f"--- [Router] LLM decision: Routing from '{last_step}' to '{next_node}' ---")
        if next_node not in ALL_NODES and next_node != END:
             print(f"--- [Router] WARNING: LLM decided on a non-existent node '{next_node}'. Ending workflow.")
             return END
        return next_node
    except Exception as e:
        print(f"--- [Router] CRITICAL ERROR: LLM router failed: {e}. Ending workflow. ---")
        return END
workflow = StateGraph(AgentState)

ALL_NODES = {
    "step_1_initial_request": step_1_initial_request, "step_2_polish_query": step_2_polish_query,
    "step_3_user_confirmation_1": step_3_user_confirmation_1, "step_4_deep_clarification": step_4_deep_clarification,
    "step_5_final_project_brief": step_5_final_project_brief, "step_6_market_analysis": step_6_market_analysis,
    "step_7_creative_ideation": step_7_creative_ideation, "step_8_internal_review_1": step_8_internal_review_1,
    "step_9_technical_planning": step_9_technical_planning, "step_10_internal_review_2": step_10_internal_review_2,
    "step_11_present_plan_to_user": step_11_present_plan_to_user, "step_12_user_feedback_loop": step_12_user_feedback_loop,
    "step_12a_decompose_plan": step_12a_decompose_plan, "step_13_task_execution": step_13_task_execution,
    "step_14_qa_loop": step_14_qa_loop, "step_15_project_completion": step_15_project_completion,
    "step_16_post_delivery_review": step_16_post_delivery_review, "step_17_reengage_workflow": step_17_reengage_workflow,
    "step_dispute_resolution": step_dispute_resolution,
}

for node_name, node_func in ALL_NODES.items():
    workflow.add_node(node_name, node_func)

workflow.set_entry_point("step_1_initial_request")

for node_name in ALL_NODES.keys():
    workflow.add_conditional_edges(node_name, intelligent_router)

app = workflow.compile()
print("--- [Graph] Intelligent workflow compiled successfully with all nodes. ---")