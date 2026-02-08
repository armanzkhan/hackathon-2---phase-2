"""
Vercel serverless function entry point for FastAPI application.

This module exports the FastAPI app for Vercel's serverless deployment.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import from src
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from src.main import app
from src.database import init_db

# Initialize database tables on cold start
init_db()

# Export the app for Vercel
# Vercel will look for a variable named 'app' or 'handler'
handler = app
