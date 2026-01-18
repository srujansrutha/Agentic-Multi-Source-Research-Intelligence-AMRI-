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
    initial_state = {"topic": request.topic}
    result = await graph_app.ainvoke(initial_state)
    
    return ResearchResponse(
        report=result.get("final_report", "Research failed."),
        source=result.get("source", "unknown")
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
        
        vector_db.add_documents(documents)
        
        return {"message": "File uploaded and indexed successfully", "chunks": len(documents)}
        
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.get("/health")
def health_check():
    return {"status": "ok"}