from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from typing import List, Optional

# This file implements the logic for intelligently splitting source code
# and documents into semantically meaningful chunks.

def chunk_file(file_content: str, file_name: str) -> List[str]:
    """
    Splits the content of a file into smaller, semantically relevant chunks.
    It automatically detects the language based on the file extension and
    uses appropriate separators for that language.
    
    Args:
        file_content: The full string content of the file.
        file_name: The name of the file (e.g., 'main.py', 'README.md').
        
    Returns:
        A list of string chunks.
    """
    print(f"--- [Chunker] Chunking file: {file_name} ---")
    
    # Map file extensions to LangChain's Language enum
    language_map = {
        ".py": Language.PYTHON,
        ".js": Language.JS,
        ".ts": Language.TS,
        ".tsx": Language.TS,
        ".md": Language.MARKDOWN,
        ".html": Language.HTML,
        ".java": Language.JAVA,
        # Add other languages as needed
    }
    
    # Determine the language from the file extension
    file_extension = "." + file_name.split(".")[-1]
    language = language_map.get(file_extension)

    if language:
        # If it's a known language, use the code-aware splitter
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=language, 
            chunk_size=500,  # The max size of a chunk
            chunk_overlap=50 # The overlap between chunks
        )
    else:
        # If the language is unknown, use a generic text splitter
        print(f"--- [Chunker] Unknown file type for '{file_name}'. Using generic splitter. ---")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
    try:
        chunks = splitter.split_text(file_content)
        print(f"--- [Chunker] Successfully split '{file_name}' into {len(chunks)} chunks. ---")
        return chunks
    except Exception as e:
        print(f"--- [Chunker] ERROR splitting file '{file_name}': {e} ---")
        return []