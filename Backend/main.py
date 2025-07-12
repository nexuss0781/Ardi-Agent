from backend.graph import app
from backend.state import AgentState

# This is the main entry point for running our Agentic AI Developer.
# In Phase 1, it allows us to perform a full, end-to-end test of the
# graph's structure and the intelligent router's logic.

def run_agent():
    """
    Initializes and runs the agent workflow with a sample request.
    """
    print("🚀 Starting Agentic AI Developer...")
    
    # 1. Define the initial state of the project
    #    This is the input that kicks off the entire process.
    initial_state: AgentState = {
        "initial_request": "Please create a simple pomodoro timer website for me.",
        # All other fields are initially empty
        "refined_query": None,
        "project_brief": None,
        "conceptual_plan": None,
        "technical_plan": None,
        "task_list": None,
        "files": None,
        "current_task": None,
        "user_feedback": None,
        "feedback_history": [],
        "last_completed_step": None,
    }

    # 2. Invoke the graph
    #    The `stream` method runs the graph step-by-step, allowing us to see
    #    the output from each node as it executes.
    final_state = None
    for event in app.stream(initial_state, stream_mode="values"):
        # The `stream` yields the entire state after each node execution.
        # We can print it to see the progress.
        print("\n" + "="*40)
        print("AGENT STATE AFTER STEP:")
        # Pretty print the event dictionary
        for key, value in event.items():
            print(f"  {key}: {value}")
        print("="*40 + "\n")
        final_state = event

    print("🏁 Agentic AI Developer has finished the run.")
    print("\n" + "="*40)
    print("FINAL PROJECT STATE:")
    for key, value in final_state.items():
            print(f"  {key}: {value}")
    print("="*40 + "\n")


if __name__ == "__main__":
    run_agent()