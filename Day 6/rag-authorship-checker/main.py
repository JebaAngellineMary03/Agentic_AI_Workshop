from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
import tempfile
import aiofiles
from typing import Optional, List
import logging
from fastapi import Form

# Import your Gemini agent
from backend.agent import GeminiResearchAgent  # Update this import path as needed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Research Paper Verification System",
    description="Academic paper verification using Gemini AI with Google Scholar integration",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Gemini agent (with error handling)
agent = None
agent_error = None

try:
    agent = GeminiResearchAgent()
    logger.info("Gemini Research Agent initialized successfully")
except Exception as e:
    agent_error = str(e)
    logger.error(f"Failed to initialize Gemini Research Agent: {e}")

class PaperSubmission(BaseModel):
    doi: Optional[str] = None
    title: Optional[str] = None
    authors: List[str] = []
    claimed_author: Optional[str] = None
    content: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Deep Learning for Natural Language Processing",
                "authors": ["John Doe", "Jane Smith"],
                "claimed_author": "John Doe",
                "content": "This paper presents a novel approach..."
            }
        }

class VerificationResponse(BaseModel):
    paper_info: dict
    authorship: dict
    ai_detection: dict
    scholar_metadata: dict
    quality_score: int
    similar_papers: List[dict]
    recommendations: List[str]
    flags: List[str]
    gemini_analysis: dict

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Research Paper Verification System",
        "status": "active" if agent else "agent_error",
        "version": "3.0.0",
        "features": [
            "Google Scholar Integration",
            "AI Content Detection", 
            "Authorship Verification",
            "RAG-based Similarity Search",
            "Gemini AI Analysis"
        ],
        "agent_status": "ready" if agent else f"error: {agent_error}"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable - Agent initialization failed: {agent_error}"
        )
    
    try:
        # Test basic agent functionality
        return {
            "status": "healthy",
            "agent": "operational",
            "gemini_api": "configured" if os.getenv('GEMINI_API_KEY') else "missing_key",
            "serpapi": "configured" if "2b832ce5d6c917c07478b99498d34635404eef913d7e0cee5dd81612fff8380b" else "missing_key"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

@app.get("/stats")
async def get_system_stats():
    """Get system statistics"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not available"
        )
    
    try:
        # Get RAG database stats if available
        stats = {
            "system_status": "operational",
            "agent_ready": True
        }
        
        # Try to get RAG stats
        try:
            rag_stats = agent.rag.get_database_stats()
            stats["database_stats"] = rag_stats
        except Exception as e:
            stats["database_stats"] = {"error": str(e)}
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.post("/verify-paper", response_model=VerificationResponse)
async def verify_paper(submission: PaperSubmission):
    """Verify a research paper submission with Google Scholar integration"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not available - check system configuration"
        )
    
    try:
        # Validate input
        if not submission.doi and not submission.title:
            raise HTTPException(
                status_code=400, 
                detail="Either DOI or title must be provided for verification"
            )
        
        if not submission.claimed_author:
            raise HTTPException(
                status_code=400,
                detail="Claimed author must be provided for authorship verification"
            )
        
        logger.info(f"Processing paper verification for: {submission.title or submission.doi}")
        
        # Process the submission
        result = await agent.process_submission(submission.dict())
        
        logger.info(f"Verification completed with quality score: {result.get('quality_score', 'N/A')}")
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing submission: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing submission: {str(e)}"
        )

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...), 
    claimed_author: str = Form(...)
):
    """Upload and analyze a PDF paper with enhanced verification"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not available"
        )
    
    # Validate file type
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported"
        )
    
    if not claimed_author:
        raise HTTPException(
            status_code=400,
            detail="Claimed author must be provided"
        )
    
    temp_file_path = None
    try:
        logger.info(f"Processing uploaded PDF: {file.filename}")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process the PDF
        result = await agent.process_pdf(temp_file_path, claimed_author)
        
        logger.info(f"PDF processing completed for: {file.filename}")
        
        return {
            "filename": file.filename,
            "size": len(content),
            "claimed_author": claimed_author,
            "analysis": result
        }
    
    except Exception as e:
        logger.error(f"Error processing PDF {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing PDF: {str(e)}"
        )
    
    finally:
        # Cleanup temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")

@app.post("/add-paper")
async def add_paper_to_database(
    title: str,
    authors: List[str],
    abstract: str = "",
    venue: str = "",
    year: int = 2024,
    keywords: List[str] = []
):
    """Add a paper to the RAG database"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not available"
        )
    
    try:
        paper_data = {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "venue": venue,
            "year": year,
            "keywords": keywords,
            "citations": 0
        }
        
        import hashlib
        paper_id = f"manual_{hashlib.md5(title.encode()).hexdigest()[:8]}"
        
        agent.rag.add_paper(paper_data, paper_id)
        
        logger.info(f"Added paper to database: {title}")
        
        return {
            "message": "Paper added successfully",
            "paper_id": paper_id,
            "title": title,
            "authors": authors
        }
    
    except Exception as e:
        logger.error(f"Error adding paper: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error adding paper: {str(e)}"
        )

@app.get("/search-papers")
async def search_papers(
    query: str,
    limit: int = 5,
    similarity_threshold: float = 0.3
):
    """Search for similar papers in the database"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not available"
        )
    
    try:
        results = agent.rag.search_similar_papers(
            query, 
            k=limit, 
            similarity_threshold=similarity_threshold
        )
        
        return {
            "query": query,
            "results_count": len(results),
            "similarity_threshold": similarity_threshold,
            "papers": results
        }
    
    except Exception as e:
        logger.error(f"Error searching papers: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching papers: {str(e)}"
        )

@app.get("/author-papers")
async def get_author_papers(author_name: str, limit: int = 10):
    """Get papers by a specific author"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not available"
        )
    
    try:
        results = agent.rag.search_by_author(author_name, k=limit)
        
        return {
            "author": author_name,
            "papers_found": len(results),
            "papers": results
        }
    
    except Exception as e:
        logger.error(f"Error searching author papers: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching author papers: {str(e)}"
        )

@app.get("/scholar-search")
async def search_google_scholar(title: str):
    """Search Google Scholar for paper metadata"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not available"
        )
    
    try:
        scholar_data = await agent.fetch_scholar_metadata(title)
        
        return {
            "query": title,
            "scholar_data": scholar_data
        }
    
    except Exception as e:
        logger.error(f"Error searching Google Scholar: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching Google Scholar: {str(e)}"
        )

# Enhanced error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "status_code": 500,
            "path": str(request.url)
        }
    )

def check_environment():
    """Check required environment variables"""
    missing_vars = []
    
    if not os.getenv('GEMINI_API_KEY'):
        missing_vars.append('GEMINI_API_KEY')
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Make sure to set these in your .env file:")
        for var in missing_vars:
            print(f"  {var}=your_api_key_here")
        print()
    else:
        print("✅ All required environment variables are set")

if __name__ == "__main__":
    print("🔍 Research Paper Verification System v3.0")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Check agent status
    if agent:
        print("✅ Gemini Research Agent: Ready")
    else:
        print(f"❌ Gemini Research Agent: Failed ({agent_error})")
    
    print()
    print("🚀 Starting server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔗 ReDoc Documentation: http://localhost:8000/redoc")
    print("💡 Health Check: http://localhost:8000/health")
    print()
    
    # Use the correct way to run with reload
    uvicorn.run(
        "main:app",  # Import string format for reload
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )