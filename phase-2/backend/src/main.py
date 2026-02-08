"""
FastAPI application entry point.

Main application with CORS middleware and router registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Full-Stack Todo Web Application REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Todo API is running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Router registration
from .routers import auth_router, tasks_router

app.include_router(auth_router)
app.include_router(tasks_router)
