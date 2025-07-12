from backend.graph import app
from backend.state import AgentState
from backend.config import load_api_keys
from backend.llm_router import activate_llm_portfolio
import pprint

# This is the main entry point for running our Agentic AI Developer.
# It initializes all necessary configurations and then invokes the graph
# with a sample request to test the full workflow skeleton.

def run_phase_1_test():
    """
    Initializes and runs the agent workflow for a Phase 1 test.
    """
    print("🚀 =============================================== 🚀")
    print("      Starting Agentic AI Developer (Phase 1 Test)   ")
    print("🚀 =============================================== 🚀\n")

    # 1. Initialize Configurations
    #    This must be done first to set up API keys and the LLM portfolio.
    print("--- [Main] Initializing configurations... ---")
    load_api_keys()
    activate_llm_portfolio()
    print("--- [Main] Configurations initialized.\n")
    
    # 2. Define the initial state of the project
    #    This is the input that kicks off the entire process.
    initial_state: AgentState = {
        "initial_request": "I need a simple website that acts like a timer for my study sessions.",
        "history_log": [],
        "dispute_raised": False,
        # All other fields are initially empty and will be populated by the agents.
        "refined_query": None,
        "user_dialogue_history": None,
        "project_brief": None,
        "research_document": None,
        "conceptual_plan": None,
        "technical_plan": None,
        "test_cases": None,
        "task_list": None,
        "current_task_id": None,
        "project_files": None,
        "review_dossier": None,
        "dispute_ruling": None,
        "user_feedback": None,
        "last_completed_step": None,
    }

    # 3. Invoke the graph
    #    The `stream` method runs the graph step-by-step. We will iterate
    #    through the events to see the output from each node as it executes.
    print("--- [Main] Invoking the workflow graph... ---\n")
    
    # The config dictionary tells the graph to start with our initial state.
    config = {"recursion_limit": 50} 
    
    final_state = None
    for event in app.stream(initial_state, config=config):
        # The `stream` yields the full state after each node execution.
        # We can pretty-print it to see the progress.
        print("\n" + "="*80)
        # The key of the dictionary is the name of the node that just ran.
        node_name = list(event.keys())[0]
        print(f"✅ State after running node: '{node_name}'")
        print("="*80)
        pprint.pprint(event[node_name])
        final_state = event[node_name]

    print("\n\n🏁 =============================================== 🏁")
    print("      Agentic AI Developer run has finished.         ")
    print("🏁 =============================================== 🏁\n")
    print("Final Project State:")
    pprint.pprint(final_state)


if __name__ == "__main__":
    # To run the test, execute this file from the root directory:
    # python main.py
    run_phase_1_test()