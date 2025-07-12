import os
from dotenv import load_dotenv

# This file handles the loading of configuration, specifically the secret API keys.

def load_api_keys():
    """
    Loads API keys from the .env file into the application's environment variables.
    This function should be called once at the very start of the application.
    """
    print("--- [Config] Loading API keys from .env file... ---")
    
    # find_dotenv will search the directory tree for the .env file
    from dotenv import find_dotenv
    env_path = find_dotenv()
    
    if not env_path:
        print("--- [Config] WARNING: .env file not found. The application may fail if API keys are not set in the environment.")
        return

    load_dotenv(env_path)
    print("--- [Config] API keys loaded into environment. ---")