import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

from backend.graph import app as agent_app
from backend.state import AgentState
from tools.agent_tools import list_files as list_workspace_files
from tools.agent_tools import read_file as read_workspace_file
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

from tools.agent_tools import STREAM_CALLBACKS # Import the shared dictionary

# ... (existing imports and app setup remain the same) ...

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, run_id: str):
        await websocket.accept()
        self.active_connections[run_id] = websocket
        # Define the callback function for this specific connection
        def stream_to_client(data: str):
            # Since this callback is called from a sync thread (the agent),
            # we must use a thread-safe way to call the async websocket method.
            # asyncio.run_coroutine_threadsafe is complex, so for simplicity,
            # we will rely on FastAPI's ability to handle this, but in a
            # high-concurrency app, a proper async queue would be better.
            try:
                # This is a simplification; a real app might need an asyncio event loop here
                asyncio.run(websocket.send_text(data))
            except RuntimeError:
                # This can happen if the event loop is already running.
                # A more robust solution involves queues. For now, we proceed.
                pass


        STREAM_CALLBACKS[run_id] = stream_to_client
        print(f"--- [API] WebSocket connected for run_id: {run_id} ---")

    def disconnect(self, run_id: str):
        del self.active_connections[run_id]
        del STREAM_CALLBACKS[run_id]
        print(f"--- [API] WebSocket disconnected for run_id: {run_id} ---")

manager = ConnectionManager()

# ... (existing Pydantic models and helper functions remain the same) ...
# ... (existing /project/start and /workspace endpoints remain the same) ...

# --- New WebSocket Endpoint ---
@app.websocket("/ws/terminal/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await manager.connect(websocket, run_id)
    try:
        while True:
            # The server keeps the connection open, listening for any potential
            # messages from the client (e.g., for interactive input in the future).
            data = await websocket.receive_text()
            # For now, we just echo it back or log it.
            print(f"--- [WS] Received from client '{run_id}': {data} ---")
            
    except WebSocketDisconnect:
        manager.disconnect(run_id)
# This file creates the main FastAPI application that serves as the backend
# for our user interface.

# --- App Initialization ---
app = FastAPI(
    title="Agentic AI Developer API",
    description="API for interacting with the LangGraph-based AI developer agent.",
    version="1.0.0",
)

# --- CORS Middleware ---
# Allows our frontend (running on a different port/domain) to communicate with this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory storage for agent runs ---
# In a production system, this would be a real database (e.g., Redis, PostgreSQL).
# For now, we'll store the state of each agent run in a simple dictionary.
agent_runs = {}

# --- Pydantic Models for API Requests ---
class StartRequest(BaseModel):
    initial_request: str

# --- Helper function to run the agent in the background ---
def run_agent_in_background(run_id: str, initial_state: AgentState):
    """
    Invokes the agent graph and updates the in-memory state as events are received.
    """
    config = {"recursion_limit": 50}
    for event in agent_app.stream(initial_state, config=config):
        agent_runs[run_id] = event # Store the latest state

# --- API Endpoints ---

@app.post("/project/start", status_code=202)
async def start_project(request: StartRequest, background_tasks: BackgroundTasks):
    """
    Starts a new agent workflow in the background.
    """
    run_id = str(uuid.uuid4())
    print(f"--- [API] Starting new agent run with ID: {run_id} ---")
    
    initial_state: AgentState = {
        "initial_request": request.initial_request,
        "history_log": [],
        "dispute_raised": False,
        # Initialize all other fields to None or default values
    }
    
    # Store the initial state immediately
    agent_runs[run_id] = {"initial": initial_state}
    
    # Run the main agent graph in a background task so the API can return immediately
    background_tasks.add_task(run_agent_in_background, run_id, initial_state)
    
    return {"message": "Agent workflow started.", "run_id": run_id}


@app.get("/project/{run_id}/status")
async def get_project_status(run_id: str):
    """
    Retrieves the latest state of a specific agent run.
    """
    if run_id not in agent_runs:
        raise HTTPException(status_code=404, detail="Project run not found.")
    
    return agent_runs[run_id]


@app.get("/workspace/files")
async def get_workspace_files(path: str = "."):
    """
    Lists the files and directories in the agent's workspace.
    """
    try:
        file_list_str = list_workspace_files(path)
        # The tool returns a string, so we split it into a list for the JSON response.
        return {"files": file_list_str.split('\n')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import Request

# ... (at the end of the file, before the uvicorn run command if any) ...

# We will need the indexer function here, which we will create in a later step.
# For now, we are just defining the endpoint.
# from backend.rag_components.indexer import index_workspace

@app.post("/workspace/index")
async def index_workspace_endpoint(request: Request):
    """
    Scans the entire /workspace directory and triggers the RAG indexing process.
    This should be called by the frontend immediately after a user selects a folder.
    """
    print("--- [API] Received request to index the entire workspace... ---")
    
    # In a real app, this would be an async background task.
    # For now, we simulate the call to a future indexer function.
    
    # In a later task, this line will be uncommented and implemented:
    # background_tasks.add_task(index_workspace)
    
    # For now, just log it.
    print("--- [API] Full workspace indexing will be implemented here. ---")
    
    return {"message": "Workspace indexing process initiated."}

# Import our new indexer function at the top of the file
from backend.rag_components.indexer import index_workspace

# Find the @app.post("/workspace/index") endpoint and replace its content
@app.post("/workspace/index", status_code=202)
async def index_workspace_endpoint(background_tasks: BackgroundTasks):
    """
    Scans the entire /workspace directory and triggers the RAG indexing process.
    This is called by the frontend immediately after a user selects a folder.
    """
    print("--- [API] Received request to index workspace. Adding to background tasks. ---")
    # Run the potentially long-running indexing process in the background
    # so the API can return an immediate response.
    background_tasks.add_task(index_workspace)
    
    return {"message": "Workspace indexing process initiated."}

@app.get("/workspace/file")
async def get_file_content(path: str):
    """
    Reads and returns the content of a specific file from the workspace.
    """
    if not path:
        raise HTTPException(status_code=400, detail="File path is required.")
    try:
        content = read_workspace_file(path)
        if content.startswith("Error:"):
            raise HTTPException(status_code=404, detail=content)
        return {"path": path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# To run this server:
# 1. Navigate to your project's root directory in the terminal.
# 2. Run the command: uvicorn api.main:app --reload
#
# The API will be available at http://127.0.0.1:8000
# You can view the auto-generated documentation at http://127.0.0.1:8000/docs