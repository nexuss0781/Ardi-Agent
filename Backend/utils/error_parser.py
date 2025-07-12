import re
from typing import Dict, Optional, Any

# This file contains helper functions to parse structured information from shell error logs.

def parse_python_traceback(stderr: str) -> Optional[Dict[str, Any]]:
    """
    Parses a standard Python traceback to find the file and line number.
    Looks for the last 'File "..."', line ...' pattern.
    
    Args:
        stderr: The standard error string from a command execution.
        
    Returns:
        A dictionary with 'file_path' and 'line_number' or None if not found.
    """
    # Regex to find the last occurrence of 'File "<path>", line <number>'
    # This is a common pattern in Python tracebacks.
    match = re.search(
        r'File "([^"]+)", line (\d+)', 
        stderr, 
        re.MULTILINE
    )
    
    if match:
        file_path = match.group(1)
        line_number = int(match.group(2))
        
        # Often paths in tracebacks are absolute from within the container.
        # We want to make them relative to the workspace for consistency.
        if '/home/agentuser/workspace/' in file_path:
            file_path = file_path.split('/home/agentuser/workspace/')[1]
            
        return {"file_path": file_path, "line_number": line_number}
        
    return None

def parse_generic_error(stderr: str) -> Optional[Dict[str, Any]]:
    """
    A generic parser for other common error formats (e.g., Node.js).
    Looks for patterns like 'path/to/file.js:line:column'.
    
    Args:
        stderr: The standard error string from a command execution.
        
    Returns:
        A dictionary with 'file_path' and 'line_number' or None if not found.
    """
    # Regex for patterns like 'file.js:12:5' or '/path/to/file.ts:12'
    match = re.search(
        r'([\/\w\.-]+\.(?:js|ts|tsx|jsx)):(\d+)',
        stderr,
        re.MULTILINE
    )

    if match:
        file_path = match.group(1)
        line_number = int(match.group(2))
        return {"file_path": file_path, "line_number": line_number}
        
    return None


def parse_error_for_location(stderr: str) -> Optional[Dict[str, Any]]:
    """
    The main parsing function. It tries different parsers to find an error location.
    
    Args:
        stderr: The standard error string.
        
    Returns:
        A dictionary with location info, or None.
    """
    if not stderr:
        return None
        
    print("--- [Error Parser] Attempting to parse error log for location... ---")
    
    # Prioritize the Python parser as it's more specific.
    location = parse_python_traceback(stderr)
    if location:
        print(f"--- [Error Parser] Found Python error at: {location} ---")
        return location
        
    # If not a Python error, try the generic one.
    location = parse_generic_error(stderr)
    if location:
        print(f"--- [Error Parser] Found generic error at: {location} ---")
        return location
        
    print("--- [Error Parser] Could not determine specific error location from logs. ---")
    return None