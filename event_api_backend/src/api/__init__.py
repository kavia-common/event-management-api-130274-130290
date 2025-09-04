"""
API package initialization.

Exports:
- app: FastAPI instance for ASGI servers (uvicorn).
- get_app: Factory to create the FastAPI application.
"""

# PUBLIC_INTERFACE
from .main import app, get_app

__all__ = ["app", "get_app"]
