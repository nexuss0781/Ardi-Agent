import os
from typing import List

# Import our RAG components
from .chunking import chunk_file
from .embedding_model import embedding_model
from .vector_store import collection as vector_store_collection
from tools.agent_tools import read_file # Use our own secure read_file

# This file contains the core logic for the indexing pipeline.

def index_file(file_path: str, workspace_root: str) -> bool:
    """
    Reads a single file, chunks it, creates embeddings, and upserts to ChromaDB.
    
    Args:
        file_path: The absolute path to the file to be indexed.
        workspace_root: The absolute path to the root of the workspace, for display names.
        
    Returns:
        True if indexing was successful, False otherwise.
    """
    print(f"--- [Indexer] Starting to index file: {file_path} ---")
    
    if not embedding_model:
        print("--- [Indexer] ERROR: Embedding model is not available. Skipping indexing. ---")
        return False
        
    try:
        # The 'read_file' tool expects a relative path, so we create it.
        relative_path = os.path.relpath(file_path, workspace_root)
        file_content = read_file(relative_path)
        
        if file_content.startswith("Error:"):
            print(f"--- [Indexer] Could not read file {relative_path}. Skipping. ---")
            return False

        # 1. Chunk the file
        chunks = chunk_file(file_content, file_name=relative_path)
        if not chunks:
            print(f"--- [Indexer] No chunks were created for {relative_path}. Skipping. ---")
            return True # Not an error if the file is empty

        # 2. Create embeddings for each chunk
        embeddings = embedding_model.encode(chunks).tolist()
        
        # 3. Prepare data for ChromaDB
        # We need a unique ID for each chunk. A good practice is hash-based or path-based.
        ids = [f"{relative_path}_chunk_{i}" for i in range(len(chunks))]
        metadata = [{"source_file": relative_path} for _ in range(len(chunks))]

        # 4. Upsert the data into the vector store
        vector_store_collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadata
        )
        
        print(f"--- [Indexer] Successfully indexed {len(chunks)} chunks for {relative_path}. ---")
        return True
        
    except Exception as e:
        print(f"--- [Indexer] CRITICAL ERROR indexing file {file_path}: {e} ---")
        return False


def index_workspace():
    """
    Scans the entire /workspace directory, ignoring specified files/folders,
    and indexes each file. This is the function for our "on-load" requirement.
    """
    print("--- [Indexer] Starting full workspace scan and index... ---")
    workspace_path = os.path.join(os.getcwd(), "workspace")
    ignore_list = {".chroma_db", ".git", "__pycache__"}

    for root, dirs, files in os.walk(workspace_path):
        # Modify the list of directories in-place to prevent os.walk from descending
        dirs[:] = [d for d in dirs if d not in ignore_list]
        
        for file in files:
            file_path = os.path.join(root, file)
            # Recursively call the single-file indexer
            index_file(file_path, workspace_root=workspace_path)
            
    print("--- [Indexer] Full workspace scan complete. ---")