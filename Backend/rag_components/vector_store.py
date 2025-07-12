import chromadb
import os

# This module initializes and configures the ChromaDB client.

# Define a persistent storage path within the workspace
# This ensures our vector data survives restarts and deployments.
_PERSIST_DIRECTORY = os.path.join(os.getcwd(), "workspace", ".chroma_db")
_COLLECTION_NAME = "project_context"

# Initialize the persistent client
print("--- [ChromaDB] Initializing persistent vector store client... ---")
client = chromadb.PersistentClient(path=_PERSIST_DIRECTORY)

# Get or create the collection for our project
print(f"--- [ChromaDB] Getting or creating collection: '{_COLLECTION_NAME}' ---")
collection = client.get_or_create_collection(name=_COLLECTION_NAME)

print("--- [ChromaDB] Vector store ready. ---")