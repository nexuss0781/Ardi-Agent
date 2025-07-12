import abc
from typing import List, Dict, Any
from backend.state import AgentState

# This file defines the abstract base classes for our agent hierarchy.
# It establishes the "contract" that all specialized agent groups must follow,
# ensuring consistency and a clear command structure.

class AgentBase(abc.ABC):
    """
    An abstract base class for all agents in the system.
    """
    
    @abc.abstractmethod
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        The main entry point for an agent to perform its work.
        
        Args:
            state: The current master state of the project.
            
        Returns:
            A dictionary containing the updates to be merged back into the state.
        """
        pass


class GroupSupervisor(AgentBase):
    """
    Represents the "Leader" of a specialized agent group.
    
    This class is responsible for receiving a high-level task from the Orchestrator,
    managing its internal team of "Laborer" models (in future phases), and
    returning the final result.
    """
    
    def __init__(self, leader_model_name: str, labor_model_list: List[str]):
        """
        Initializes the Supervisor with its designated models from the taxonomy.
        
        Args:
            leader_model_name: The logical name (from config.yaml) of the leader model.
            labor_model_list: A list of logical names for the laborer models.
        """
        self.leader_model_name = leader_model_name
        self.labor_model_list = labor_model_list
        # In future phases, we would initialize the LLMs here.
        # For Phase 1, we just store their names.

    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        A stubbed execution method for Phase 1.
        It logs the activation of the supervisor and its designated leader model.
        """
        # Get the name of the child class (e.g., "UserEngagementGroup") for logging
        class_name = self.__class__.__name__
        
        print(f"--- [Supervisor Stub] Executing: {class_name} ---")
        print(f"    - Leader Model: {self.leader_model_name}")
        print(f"    - Labor Models Available: {len(self.labor_model_list)}")
        
        # In a real implementation, this is where the supervisor would use its
        # leader model to break down the task from the state and delegate to
        # its labor models.
        
        # For Phase 1, we return a simple, hardcoded update.
        # The key is a generic placeholder to show data was produced.
        return {
            f"{class_name}_output": "This is a hardcoded result from the stubbed supervisor."
        }