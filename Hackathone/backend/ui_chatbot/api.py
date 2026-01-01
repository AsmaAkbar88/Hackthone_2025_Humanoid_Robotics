"""
FastAPI Chatbot API for Docusaurus Book
Bridges frontend chat UI to existing RAG backend (agent_retriev.py)
"""

import sys
import os
from typing import Optional
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, constr
from dotenv import load_dotenv
import logging

# Add parent directory to path to import agent_retriev
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import existing RAG agent
try:
    from agent_retriev import RAGAgent
except ImportError as e:
    logging.error(f"Failed to import RAGAgent: {e}")
    logging.error("Make sure agent_retriev.py is in the backend directory")
    raise

# Load environment variables from backend folder
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Docusaurus Book Chatbot API",
    description="API for RAG-powered chatbot integrated into Physical AI & Humanoid Robotics Docusaurus book",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local development (Docusaurus)
        "https://asmaakbar88.vercel.app",  # Production Docusaurus URL
        "http://localhost",            # Fallback for local
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ============================================================================
# Pydantic Models
# ============================================================================

class PageContext(BaseModel):
    """Optional page context metadata"""
    page_url: Optional[str] = Field(None, description="Current page URL")
    page_title: Optional[str] = Field(None, description="Current page title")


class ChatRequest(BaseModel):
    """Request body for /chat endpoint"""
    query: constr(min_length=5, max_length=2000) = Field(..., description="User's question or message")
    highlighted_text: Optional[constr(max_length=500)] = Field(
        None,
        description="Highlighted text from book for context"
    )
    context: Optional[PageContext] = Field(None, description="Optional page metadata")


class ChatResponse(BaseModel):
    """Response body for /chat endpoint"""
    response_id: str
    query_id: str
    content: str
    generation_time: float
    confidence_score: float
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error type/category")
    message: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Programmatic error code")


class ServiceHealth(BaseModel):
    """Service dependency status"""
    qdrant: bool
    openai: bool
    cohere: bool
    overall: bool


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Overall health status")
    details: ServiceHealth


# ============================================================================
# Initialize RAG Agent
# ============================================================================

# Initialize single RAG agent instance for efficiency
try:
    rag_agent = RAGAgent()
    logger.info("RAG Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG Agent: {e}")
    raise RuntimeError(f"Failed to initialize RAG Agent: {e}")


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint
    Verifies the status of all dependencies (Qdrant, Cohere, OpenAI)
    """
    try:
        # Get health status from RAG agent
        status = rag_agent.health_check()

        return HealthResponse(
            status="healthy" if status["overall"] else "unhealthy",
            details=ServiceHealth(
                qdrant=status.get("qdrant", False),
                openai=status.get("openai", False),
                cohere=status.get("cohere", False),
                overall=status.get("overall", False)
            )
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Health check failed"
        )


@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        200: {"description": "Successful response", "model": ChatResponse},
        400: {"description": "Bad request", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    },
    tags=["Chat"]
)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that queries the RAG backend to get a response based on book content.

    Optionally includes highlighted text as context for the query.

    Args:
        request: ChatRequest containing query, optional highlighted_text, and context

    Returns:
        ChatResponse with AI-generated answer based on book content

    Raises:
        HTTPException: For validation errors or backend failures
    """
    try:
        # Validate highlighted text length (if provided)
        if request.highlighted_text and len(request.highlighted_text) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationError",
                    "message": "Highlighted text must not exceed 500 characters",
                    "code": "HIGHLIGHT_TOO_LONG"
                }
            )

        # Construct enhanced query with highlighted context
        if request.highlighted_text:
            enhanced_query = f"Context: {request.highlighted_text}\n\nQuestion: {request.query}"
            logger.info(f"Processing query with highlighted context: {request.query[:50]}... (highlighted: {request.highlighted_text[:30]}...)")
        else:
            enhanced_query = request.query
            logger.info(f"Processing query: {request.query[:50]}...")

        # Query RAG agent
        try:
            response = rag_agent.query(enhanced_query)
        except ValueError as e:
            # Check if it's an embedding error
            error_msg = str(e)
            if "embedding" in error_msg.lower() or "cohere" in error_msg.lower() or "gemini" in error_msg.lower():
                logger.error(f"Embedding error: {e}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail={
                        "error": "EmbeddingServiceUnavailable",
                        "message": "Embedding service is busy. Please wait a few seconds and try again.",
                        "code": "EMBEDDING_ERROR"
                    }
                )
            # Validation error from RAG agent
            logger.error(f"RAG agent validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationError",
                    "message": str(e),
                    "code": "QUERY_VALIDATION_ERROR"
                }
            )
        except Exception as e:
            # Backend error - show actual error
            error_str = str(e)
            logger.error(f"RAG agent error: {error_str}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "ServiceUnavailable",
                    "message": f"Backend error: {error_str[:100]}",
                    "code": "SERVICE_UNAVAILABLE"
                }
            )

        # Convert response to ChatResponse
        chat_response = ChatResponse(
            response_id=response.response_id,
            query_id=response.query_id,
            content=response.content,
            generation_time=response.generation_time,
            confidence_score=response.confidence_score,
            timestamp=response.timestamp.isoformat() if response.timestamp else datetime.utcnow().isoformat()
        )

        logger.info(
            f"Query processed successfully: "
            f"generation_time={response.generation_time:.2f}s, "
            f"confidence={response.confidence_score:.2f}"
        )

        return chat_response

    except HTTPException:
        # Re-raise HTTP exceptions (already formatted)
        raise
    except Exception as e:
        # Unexpected error
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred. Please try again later.",
                "code": "INTERNAL_ERROR"
            }
        )


# ============================================================================
# Startup and Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup and verify connections"""
    logger.info("Starting Docusaurus Book Chatbot API...")

    # Verify RAG agent health
    health = rag_agent.health_check()
    if health["overall"]:
        logger.info("All dependencies are healthy")
    else:
        logger.warning(
            f"Some dependencies are unhealthy: {health}. "
            "Chatbot may not function correctly."
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown"""
    logger.info("Shutting down Docusaurus Book Chatbot API...")


# ============================================================================
# Root endpoint
# ============================================================================

@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Docusaurus Book Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn

    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
