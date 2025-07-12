import yaml
import os
from typing import Dict, Any

# This file implements the TaxonomyRegistry, a singleton class responsible
# for loading and providing access to our entire agent hierarchy.

class TaxonomyRegistry:
    """
    A singleton class that loads the llm_taxonomy.yaml file once and provides
    a structured, easily accessible dictionary of our agent hierarchy.
    """
    _instance = None
    _registry: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaxonomyRegistry, cls).__new__(cls)
            cls._instance._load_registry()
        return cls._instance

    def _load_registry(self):
        """Loads and parses the llm_taxonomy.yaml file."""
        print("--- [Registry] Initializing Taxonomy Registry... ---")
        
        # Build the absolute path to the taxonomy file
        taxonomy_path = os.path.join(os.path.dirname(__file__), 'llm_taxonomy.yaml')
        
        if not os.path.exists(taxonomy_path):
            raise FileNotFoundError(f"CRITICAL ERROR: The taxonomy file was not found at {taxonomy_path}")

        with open(taxonomy_path, 'r') as f:
            self._registry = yaml.safe_load(f)
            
        print(f"--- [Registry] Taxonomy loaded successfully with {len(self._registry)} top-level groups. ---")

    def get_registry(self) -> Dict[str, Any]:
        """Returns the entire loaded taxonomy dictionary."""
        return self._registry

    def get_group_details(self, group_name: str) -> Dict[str, Any]:
        """
        Returns the specific configuration dictionary for a given group.
        
        Args:
            group_name: The name of the group (e.g., "user_engagement_group").
            
        Returns:
            A dictionary with the group's details, or an empty dict if not found.
        """
        details = self._registry.get(group_name)
        if not details:
            print(f"--- [Registry] WARNING: No details found for group: {group_name}")
            return {}
        return details

# You can create a single instance for the application to import and use.
taxonomy_registry = TaxonomyRegistry()