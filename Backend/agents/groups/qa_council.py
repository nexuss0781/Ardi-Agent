from typing import Dict, Any, List
from langchain_groq import ChatGroq

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt, create_agent
from tools.agent_tools import read_file, list_files

# This defines the sequence in which the auditors will run.
AUDIT_SEQUENCE = [
    ("code_quality_auditor", "Code Quality Audit"),
    ("security_auditor", "Security Audit"),
    ("performance_auditor", "Performance Audit"),
    ("ux_logic_auditor", "UX/Logic Audit"),
    ("antagonistic_tester", "Antagonistic Testing"),
]

class QACouncil(GroupSupervisor):
    """
    The supervisor for the Quality Assurance Council.
    This agent now orchestrates its five sub-groups to perform a comprehensive review.
    """
    
    def _run_auditor(self, auditor_key: str, state: AgentState) -> str:
        """Helper function to execute a single auditor and return its feedback."""
        
        # 1. Get the details for the specific sub-group auditor
        auditor_details = self.group_details.get("sub_groups", {}).get(auditor_key, {})
        if not auditor_details:
            return f"Error: Could not find details for auditor '{auditor_key}'."
            
        leader_model_name = auditor_details.get("leader", {}).get("unique_name", "fast-router")
        print(f"--- [QA Council] Running sub-group: {auditor_key} with leader: {leader_model_name} ---")

        # 2. Initialize LLM and tools
        llm = ChatGroq(temperature=0.0, model_name=leader_model_name)
        system_prompt = load_prompt(f"{auditor_key}.md")
        tools = [read_file, list_files]
        
        # 3. Create and invoke the auditor agent
        agent_executor = create_agent(llm, system_prompt, tools)
        
        # The input is generic for most auditors; they use tools to get what they need.
        input_content = "Please perform your audit based on the files in the workspace. The primary file under review is likely `src/main.py` or a similar core file. The planning documents are `conceptual_plan.md` and `technical_plan.md`."

        try:
            response = agent_executor.invoke({"input": input_content})
            return response['output']
        except Exception as e:
            return f"Error during {auditor_key} execution: {e}"


    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Overrides the stub method to run the full, multi-step audit process,
        starting with automated tests.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")
        
        full_feedback: List[str] = []
        final_verdict = "Approved"

        # Step 1: Run automated tests first.
        test_results_feedback = self._run_automated_tests(state)
        full_feedback.append(f"## Automated Test Results\n{test_results_feedback}")

        if "failed" in test_results_feedback.lower():
            final_verdict = "Revision Required"
        else:
            # Step 2: If tests pass, proceed with the manual audit sequence.
            print("--- [QA Council] Proceeding to manual audits... ---")
            for auditor_key, audit_name in AUDIT_SEQUENCE:
                feedback = self._run_auditor(auditor_key, state)
                full_feedback.append(f"## {audit_name}\n{feedback}")
                
                if "Revision Required" in feedback and auditor_key != "antagonistic_tester":
                    print(f"--- [QA Council] '{audit_name}' requires revision. Halting review. ---")
                    final_verdict = "Revision Required"
                    break
        
        consolidated_feedback = "\n\n---\n\n".join(full_feedback)
        
        final_dossier_content = f"# QA Council Review Dossier\n\n{consolidated_feedback}\n\n---\n\n**FINAL VERDICT: {final_verdict}**"

        return {
            "history_log": state.get("history_log", []) + [f"The {self.group_name} has completed its review. Verdict: {final_verdict}"],
            "review_dossier": {"feedback": final_dossier_content}
        }
        
    def _run_automated_tests(self, state: AgentState) -> str:
        """Helper function to run the automated tests defined in the technical plan."""
        print(f"--- [QA Council] Running Automated Tests... ---")
        
        # In a real system, this agent would read the `test_cases` from the
        # technical plan and construct the correct command (e.g., "pytest", "npm test").
        # For Phase 4, we will simulate this by running a generic command.
        
        test_command = "python -m unittest discover tests" # A common Python test command
        
        # We can directly call the tool function here
        from tools.agent_tools import execute_in_sandbox
        
        # We need a run_id for streaming, we can use a generic one for this internal process
        run_id = f"qa-test-run-{state.get('initial_request', 'test')[:10]}"

        test_results = execute_in_sandbox(test_command, run_id)

        # A simple check to see if the tests passed. A real system would parse the output.
        if "FAILED" in test_results or "Error" in test_results:
            print(f"--- [QA Council] Automated Tests FAILED. ---")
            return f"Automated tests failed.\n\n{test_results}"
        else:
            print(f"--- [QA Council] Automated Tests PASSED. ---")
            return "All automated tests passed."