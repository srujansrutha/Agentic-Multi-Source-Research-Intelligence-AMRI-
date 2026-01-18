import os
import shutil
import uuid
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader

from app.core.config import settings
from app.models import ResearchRequest, ResearchResponse
from app.agent.graph import graph_app
from app.services.vector_db import vector_db

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """Run the research agent."""
    thread_id = str(uuid.uuid4())
    
    # Initialize state with HITL flag
    initial_state = {
        "topic": request.topic, 
        "enable_hitl": request.enable_hitl
    }
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Use invoke (sync) instead of ainvoke for RedisSaver compatibility
        result = graph_app.invoke(initial_state, config=config)
        
        # Check if we are done or paused
        snapshot = graph_app.get_state(config)
        next_step = snapshot.next
        
        status = "completed"
        if next_step and "human_review" in next_step:
            status = "paused"
        
        final_report = result.get("final_report")
        if status == "paused":
            final_report = "WAITING FOR HUMAN INPUT... (Search & RAG Completed)"

        return ResearchResponse(
            report=final_report,
            source=result.get("source", "unknown"),
            thread_id=thread_id,
            status=status
        )
    except Exception as e:
        return ResearchResponse(
            report=f"Error: {str(e)}",
            source="error",
            thread_id=thread_id,
            status="error"
        )

@app.post("/research/resume/{thread_id}", response_model=ResearchResponse)
async def resume_research(thread_id: str, feedback: str):
    """Resume a paused research thread with human feedback."""
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Check current state
        snapshot = graph_app.get_state(config)
        if not snapshot.next:
            return ResearchResponse(
                report="Thread already completed or invalid.",
                source="unknown",
                thread_id=thread_id,
                status="error"
            )
        
        # Update state with feedback
        graph_app.update_state(config, {"human_feedback": feedback}, as_node="human_review")
        
        # Resume using invoke
        result = graph_app.invoke(None, config=config)
        
        return ResearchResponse(
            report=result.get("final_report", "Research failed."),
            source=result.get("source", "unknown"),
            thread_id=thread_id,
            status="completed"
        )
    except Exception as e:
        return ResearchResponse(
            report=f"Error: {str(e)}",
            source="error",
            thread_id=thread_id,
            status="error"
        )

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload PDF and ingest into Vector DB."""
    temp_filename = f"temp_{uuid.uuid4()}.pdf"
    
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        loader = PyPDFLoader(temp_filename)
        documents = loader.load_and_split()
        
        # Update metadata with original filename
        for doc in documents:
            doc.metadata["source"] = file.filename
        
        vector_db.add_documents(documents)
        
        return {"message": "File uploaded and indexed successfully", "chunks": len(documents)}
        
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.get("/health")
def health_check():
    return {"status": "ok"}
