from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
import litellm
import docker
import time
from typing import Callable, Optional, Dict, Any

# Import our new error parser
from backend.utils.error_parser import parse_error_for_location

# ... (other tools like search, file I/O, etc. remain the same) ...


# --- Tool 4: Secure Code Execution Sandbox (Upgraded for Structured Output) ---

# Initialize the Docker client from the environment.
try:
    _docker_client = docker.from_env()
except docker.errors.DockerException:
    print("--- [Tool] WARNING: Docker is not running or accessible. The 'execute_in_sandbox' tool will not be available.")
    _docker_client = None

_DOCKER_IMAGE_NAME = "agentic_sandbox:latest"

def _build_sandbox_image_if_needed():
    """Helper function to build the Docker image if it doesn't already exist."""
    if not _docker_client: return
    try:
        _docker_client.images.get(_DOCKER_IMAGE_NAME)
    except docker.errors.ImageNotFound:
        print(f"--- [Tool] Sandbox image '{_DOCKER_IMAGE_NAME}' not found. Building now...")
        try:
            _docker_client.images.build(path="./sandbox", tag=_DOCKER_IMAGE_NAME, rm=True)
            print(f"--- [Tool] Sandbox image built successfully. ---")
        except docker.errors.BuildError as e:
            print(f"--- [Tool] CRITICAL ERROR: Could not build Docker image. Error: {e}")
            raise

STREAM_CALLBACKS: dict[str, Optional[Callable]] = {}

@tool
def execute_in_sandbox(command: str, run_id: str) -> Dict[str, Any]:
    """
    Executes a shell command inside a secure, isolated Docker sandbox.
    It streams the output in real-time and returns a structured object
    indicating success or failure, including parsed error locations.
    
    Args:
        command: The shell command to execute.
        run_id: The unique ID of the agent run for real-time streaming.
        
    Returns:
        A dictionary with the execution status, logs, and optional error details.
    """
    if not _docker_client:
        return {"status": "error", "error": "Docker not available."}
        
    _build_sandbox_image_if_needed()
    
    workspace_volume_path = os.path.abspath(_WORKSPACE_DIR)
    container = None
    
    try:
        print(f"--- [Tool] Creating sandbox container for run '{run_id}' to execute: '{command}' ---")
        container = _docker_client.containers.run(
            image=_DOCKER_IMAGE_NAME,
            command=["/bin/sh", "-c", command],
            volumes={workspace_volume_path: {'bind': '/home/agentuser/workspace', 'mode': 'rw'}},
            working_dir='/home/agentuser/workspace',
            detach=True,
            remove=False
        )
        
        # Stream logs in real-time
        stream_callback = STREAM_CALLBACKS.get(run_id)
        if stream_callback:
            for line in container.logs(stream=True, follow=True):
                stream_callback(line.decode('utf-8'))
        
        # Get final results
        result = container.wait()
        exit_code = result['StatusCode']
        stdout = container.logs(stdout=True, stderr=False).decode('utf-8')
        stderr = container.logs(stdout=False, stderr=True).decode('utf-8')
        
        print(f"--- [Tool] Sandbox execution finished with exit code: {exit_code}. ---")

        if exit_code == 0:
            return {"status": "success", "stdout": stdout, "stderr": stderr}
        else:
            # If the command failed, try to parse the error location from stderr
            error_location = parse_error_for_location(stderr)
            return {
                "status": "error", 
                "stdout": stdout, 
                "stderr": stderr,
                "error_details": error_location  # This will be None or {'file_path': '...', 'line_number': ...}
            }

    except Exception as e:
        return {"status": "error", "error": f"An unexpected error occurred: {e}"}
    finally:
        if container:
            try:
                container.stop(timeout=5)
                container.remove()
            except docker.errors.APIError as e:
                print(f"--- [Tool] Warning: Could not clean up container '{container.short_id}'. Error: {e}")
# --- Tool 3: Sketching / Diagramming Tool ---

# A concise prompt to instruct the LLM on how to generate Mermaid syntax.
_MERMAID_PROMPT_TEMPLATE = """
You are a specialist in creating diagrams. Your sole task is to convert a user's description into valid Mermaid.js syntax.
You must only output the Mermaid code itself, inside a '```mermaid' code block. Do not include any other text, explanations, or apologies.

Description:
"{description}"
"""

@tool
def generate_mermaid_syntax(description: str, file_path: str) -> str:
    """
    Takes a natural language description of a process or structure,
    converts it into Mermaid.js diagram syntax, and saves it to a file.
    
    Args:
        description: A clear description of the diagram to create 
                     (e.g., "A flowchart with three steps: A goes to B, B goes to C").
        file_path: The relative path within the workspace to save the .md file
                   (e.g., 'diagrams/workflow.md').
    """
    print(f"--- [Tool] Generating Mermaid syntax for: '{description}' ---")
    try:
        # Use a fast and free LLM for this specialized task.
        # We call litellm directly here as it's a simple, self-contained task.
        response = litellm.completion(
            model="fast-router", # Uses the alias from our config.yaml
            messages=[{
                "role": "user",
                "content": _MERMAID_PROMPT_TEMPLATE.format(description=description)
            }],
            temperature=0.0
        )
        
        # Extract the content from the response
        mermaid_syntax = response.choices.message.content
        
        # Clean up the output to ensure it's just the code block
        if "```mermaid" in mermaid_syntax:
             mermaid_syntax = "```mermaid" + mermaid_syntax.split("```mermaid")[1]
        if "```" in mermaid_syntax:
            mermaid_syntax = mermaid_syntax.split("```")[0] + "```"

        print(f"--- [Tool] Syntax generated. Writing to file: '{file_path}' ---")
        
        # Use our existing, secure write_file tool to save the output
        write_result = write_file(path=file_path, content=mermaid_syntax)
        
        return f"Mermaid diagram syntax generated and saved. File system response: '{write_result}'"
        
    except Exception as e:
        return f"An error occurred during Mermaid diagram generation: {e}"
# This file will contain the implementation of the core, custom-wrapped tools
# that our intelligent agents will use to perform actions.

# --- Tool 1: Advanced Web Search ---

# First, we initialize the base tool from the community library.
# We do this once here so it can be reused.
_search_tool_instance = DuckDuckGoSearchRun()

@tool
def advanced_web_search(query: str) -> str:
    """
    Performs a web search using DuckDuckGo to find information on a given topic.
    This tool is best for research, finding technologies, or understanding concepts.
    
    Args:
        query: The topic or question to search for.
    """
    print(f"--- [Tool] Executing Web Search for: '{query}' ---")
    try:
        # We call the .run() method of the initialized tool instance.
        results = _search_tool_instance.run(query)
        print(f"--- [Tool] Web Search completed. ---")
        return results
    except Exception as e:
        print(f"--- [Tool] ERROR in Web Search: {e} ---")
        return f"An error occurred during the web search: {e}"
import os

# --- Tool 2: Secure File I/O Suite ---

# Define a dedicated, sandboxed directory for the agent's file operations.
# This is a critical security measure to prevent the agent from accessing
# unintended files on the host system.
_WORKSPACE_DIR = os.path.join(os.getcwd(), "workspace")

# Ensure the workspace directory exists upon module load.
os.makedirs(_WORKSPACE_DIR, exist_ok=True)

def _get_safe_path(path: str) -> str:
    """
    A helper function to ensure the file path is safe and within the workspace.
    It prevents directory traversal attacks (e.g., trying to access ../../).
    
    Args:
        path: The relative path from the user or agent.
        
    Returns:
        The absolute, safe path if valid.
        
    Raises:
        ValueError: If the path is outside the workspace.
    """
    # os.path.join handles the initial path construction.
    # os.path.normpath cleans up the path (e.g., a/b/../c -> a/c).
    absolute_path = os.path.normpath(os.path.join(_WORKSPACE_DIR, path))
    
    # The most important check: ensure the resolved path still starts with
    # our designated WORKSPACE_DIR path.
    if not absolute_path.startswith(_WORKSPACE_DIR):
        raise ValueError(f"Security Error: Path '{path}' attempts to access files outside of the designated workspace.")
        
    return absolute_path
# Import the single-file indexer at the top of the file
from backend.rag_components.indexer import index_file as trigger_file_index

# Find the `write_file` tool and modify it to call the indexer
@tool
def write_file(path: str, content: str) -> str:
    """
    Writes content to a specified file within the secure workspace.
    If the file or directories do not exist, they will be created.
    **After writing, this tool automatically triggers the indexing process for the file.**
    """
    print(f"--- [Tool] Attempting to write to file: '{path}' ---")
    try:
        safe_path = _get_safe_path(path)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # --- RAG INTEGRATION ---
        # After a successful write, trigger the indexing process for this file.
        # We do this asynchronously in a real app, but for simplicity here we call it directly.
        print(f"--- [Tool] File written. Triggering RAG indexing for {path}... ---")
        trigger_file_index(file_path=safe_path, workspace_root=_WORKSPACE_DIR)
        
        return f"Successfully wrote to {path} and triggered indexing."
        
    except Exception as e:
        return f"An error occurred while writing to file: {e}"

@tool
def read_file(path: str) -> str:
    """
    Reads the entire content from a specified file within the secure workspace.
    
    Args:
        path: The relative path of the file to read (e.g., 'plans/conceptual_plan.md').
    """
    print(f"--- [Tool] Attempting to read from file: '{path}' ---")
    try:
        safe_path = _get_safe_path(path)
        
        if not os.path.exists(safe_path):
            return f"Error: File not found at path '{path}'."
            
        with open(safe_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        return f"An error occurred while reading file: {e}"

@tool
def list_files(path: str = ".") -> str:
    """
    Lists all files and subdirectories within a given path inside the secure workspace.
    
    Args:
        path: The relative path of the directory to list (e.g., 'plans/' or '.'). 
              Defaults to the root of the workspace.
    """
    print(f"--- [Tool] Attempting to list directory: '{path}' ---")
    try:
        safe_path = _get_safe_path(path)
        
        if not os.path.isdir(safe_path):
            return f"Error: The specified path '{path}' is not a directory."
            
        files = os.listdir(safe_path)
        
        if not files:
            return f"The directory '{path}' is empty."
        
        return "\n".join(files)
        
    except Exception as e:
        return f"An error occurred while listing the directory: {e}"
        
 # Import the RAG components we need at the top of the file
from backend.rag_components.embedding_model import embedding_model
from backend.rag_components.vector_store import collection as vector_store_collection

# --- Tool 5: Context Retrieval (The Agent's Memory) ---

@tool
def retrieve_context(query: str, n_results: int = 5) -> str:
    """
    Searches the project's vector database to retrieve code chunks and
    documentation that are semantically relevant to a given query.
    This is the primary tool for an agent to "remember" how the codebase works.
    
    Args:
        query: A natural language question or topic about the codebase.
        n_results: The number of relevant chunks to retrieve. Defaults to 5.
    """
    print(f"--- [Tool] Retrieving context for query: '{query}' ---")
    
    if not embedding_model or not vector_store_collection:
        return "Error: RAG system is not available. Could not retrieve context."
        
    try:
        # 1. Embed the query
        query_embedding = embedding_model.encode(query).tolist()
        
        # 2. Query ChromaDB for the most similar chunks
        results = vector_store_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # 3. Format the results into a single, clean string for the LLM
        context_str = "--- CONTEXTUAL INFORMATION ---\n\n"
        if not results or not results.get("documents"):
            return "No relevant context found in the knowledge base."

        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]
            source_file = metadata.get("source_file", "Unknown source")
            
            context_str += f"--- Snippet from `{source_file}` ---\n"
            context_str += f"{doc}\n\n"
            
        context_str += "--- END OF CONTEXTUAL INFORMATION ---"
        
        print(f"--- [Tool] Successfully retrieved {len(results['documents'][0])} context snippets. ---")
        return context_str

    except Exception as e:
        error_message = f"An error occurred while retrieving context: {e}"
        print(f"--- [Tool] ERROR: {error_message} ---")
        return error_message
        
import litellm

# --- Tool 3: Sketching / Diagramming Tool ---

# A concise prompt to instruct the LLM on how to generate Mermaid syntax.
_MERMAID_PROMPT_TEMPLATE = """
You are a specialist in creating diagrams. Your sole task is to convert a user's description into valid Mermaid.js syntax.
You must only output the Mermaid code itself, inside a '```mermaid' code block. Do not include any other text, explanations, or apologies.

Description:
"{description}"
"""

@tool
def generate_mermaid_syntax(description: str, file_path: str) -> str:
    """
    Takes a natural language description of a process or structure,
    converts it into Mermaid.js diagram syntax, and saves it to a file.
    
    Args:
        description: A clear description of the diagram to create 
                     (e.g., "A flowchart with three steps: A goes to B, B goes to C").
        file_path: The relative path within the workspace to save the .md file
                   (e.g., 'diagrams/workflow.md').
    """
    print(f"--- [Tool] Generating Mermaid syntax for: '{description}' ---")
    try:
        # Use a fast and free LLM for this specialized task.
        # We call litellm directly here as it's a simple, self-contained task.
        response = litellm.completion(
            model="fast-router", # Uses the alias from our config.yaml
            messages=[{
                "role": "user",
                "content": _MERMAID_PROMPT_TEMPLATE.format(description=description)
            }],
            temperature=0.0
        )
        
        # Extract the content from the response
        mermaid_syntax = response.choices.message.content
        
        # Clean up the output to ensure it's just the code block
        if "```mermaid" in mermaid_syntax:
             mermaid_syntax = "```mermaid" + mermaid_syntax.split("```mermaid")[1]
        if "```" in mermaid_syntax:
            mermaid_syntax = mermaid_syntax.split("```")[0] + "```"

        print(f"--- [Tool] Syntax generated. Writing to file: '{file_path}' ---")
        
        # Use our existing, secure write_file tool to save the output
        write_result = write_file(path=file_path, content=mermaid_syntax)
        
        return f"Mermaid diagram syntax generated and saved. File system response: '{write_result}'"
        
    except Exception as e:
        return f"An error occurred during Mermaid diagram generation: {e}"