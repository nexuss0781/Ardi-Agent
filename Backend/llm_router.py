import litellm
import os

# This module centralizes the setup and activation of the LiteLLM router.

def activate_llm_portfolio():
    """
    Sets the LiteLLM configuration from the master config.yaml file.
    This must be called once when the application starts up.
    """
    print("--- [Router] Activating LLM portfolio from config.yaml... ---")
    
    # Build the absolute path to the config.yaml file relative to this file's location
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"CRITICAL ERROR: The LiteLLM configuration file was not found at {config_path}")

    try:
        litellm.config_path = config_path
        print(f"--- [Router] LiteLLM configured successfully with: {config_path} ---")
    except Exception as e:
        print(f"--- [Router] CRITICAL ERROR: Could not load config.yaml into LiteLLM. Error: {e} ---")
        raise