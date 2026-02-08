"""
Hugging Face Space entry point for FastAPI application.

This is the main entry point that Hugging Face Spaces will use.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Print environment variables for debugging (remove in production)
print("=" * 50)
print("Environment Variables Check:")
print(f"DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")
print(f"BETTER_AUTH_SECRET exists: {bool(os.getenv('BETTER_AUTH_SECRET'))}")
print(f"CORS_ORIGINS exists: {bool(os.getenv('CORS_ORIGINS'))}")
print(f"ENVIRONMENT: {os.getenv('ENVIRONMENT', 'not set')}")
print("=" * 50)

try:
    from src.main import app
    from src.database import init_db

    # Initialize database tables
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")

except Exception as e:
    print(f"ERROR during initialization: {e}")
    import traceback
    traceback.print_exc()
    raise

# This is what Hugging Face Spaces or uvicorn will use
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
