from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routes.tasks import router as tasks_router
from .routes.auth import router as auth_router
from .routes.chat import router as chat_router
from .mcp_server import server as mcp_server
from ..config import settings
from ..utils.error_handlers import add_exception_handlers
from ..middleware.security import SecurityHeadersMiddleware

# Reduce SQLAlchemy logging to reduce noise
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for FastAPI application.

    Handles startup and shutdown events.
    """
    # Startup
    print("Starting up Todo Backend API...")

    # Add exception handlers
    add_exception_handlers(app)

    yield

    # Shutdown
    print("Shutting down Todo Backend API...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan
    )

    # Add security headers middleware first
    app.add_middleware(SecurityHeadersMiddleware)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(tasks_router, prefix=settings.api_prefix)
    app.include_router(auth_router, prefix=settings.api_prefix)
    app.include_router(chat_router, prefix=settings.api_prefix)

    @app.get("/")
    async def root():
        """Root endpoint for the API."""
        return {
            "message": "Welcome to the Todo Backend API",
            "app_name": settings.app_name,
            "version": "1.0.0"
        }

    @app.get("/health", include_in_schema=False)
    async def health():
        """Health check endpoint for Kubernetes probes."""
        return {"status": "healthy"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )