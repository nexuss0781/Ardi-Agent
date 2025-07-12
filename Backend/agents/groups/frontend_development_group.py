from typing import Dict, Any, List
from langchain_groq import ChatGroq

from backend.agents.base import GroupSupervisor
from backend.state import AgentState
from ..utils import load_prompt, create_agent
from tools.agent_tools import (
    read_file, 
    write_file, 
    list_files, 
    execute_in_sandbox
)

class FrontendDevelopmentGroup(GroupSupervisor):
    """
    The supervisor for the Frontend Development Group.
    This agent is now intelligent and can execute coding tasks.
    """
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Overrides the stub method to implement the task execution logic.
        """
        print(f"--- [Agent] Executing: {self.group_name} ---")

        # 1. Get the full task list and find the next available task
        task_list = state.get("task_list", [])
        completed_tasks = [task for task in task_list if task.get("status") == "completed"]
        completed_task_ids = {task['id'] for task in completed_tasks}

        next_task = None
        for task in task_list:
            if task.get("status") != "completed" and task.get("group") == "frontend_development_group":
                if all(dep_id in completed_task_ids for dep_id in task.get("dependencies", [])):
                    next_task = task
                    break
        
        if not next_task:
            print(f"--- [Agent] {self.group_name}: No available tasks found. Passing control. ---")
            return {"last_completed_step": "step_13_task_execution"}

        print(f"--- [Agent] {self.group_name}: Starting task '{next_task['id']}: {next_task['description']}' ---")

        # 2. Initialize the LLM and tools
        llm = ChatGroq(temperature=0.0, model_name=self.leader_model.get("unique_name"))
        system_prompt = load_prompt("frontend_developer.md")
        tools = [read_file, write_file, list_files, execute_in_sandbox]
        
        # 3. Create the agent executor
        agent_executor = create_agent(llm, system_prompt, tools)
        
        # 4. Prepare the input for the agent
        input_content = (
            f"Your current task is:\n"
            f"ID: {next_task['id']}\n"
            f"Description: {next_task['description']}\n\n"
            f"Please implement this task. Read the technical_plan.md and conceptual_plan.md "
            f"if you need more context. Use your tools to create the necessary UI components."
        )

        # 5. Invoke the agent to perform the coding task
        try:
            response = agent_executor.invoke({"input": input_content})
            task_result = response['output']
            
            # 6. Update the task's status to 'completed'
            for task in task_list:
                if task['id'] == next_task['id']:
                    task['status'] = 'completed'
                    task['result'] = task_result
                    break
            
        except Exception as e:
            print(f"--- [Agent] CRITICAL ERROR during task '{next_task['id']}': {e} ---")
            for task in task_list:
                if task['id'] == next_task['id']:
                    task['status'] = 'error'
                    task['result'] = str(e)
                    break

        # 7. Return the updated task list
        return {
            "history_log": state.get("history_log", []) + [f"{self.group_name} completed task: {next_task['id']}"],
            "task_list": task_list,
            "last_completed_step": "step_13_task_execution"
        }
