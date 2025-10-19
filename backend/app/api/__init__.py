"""
API Package
===========

Main API package for the LogViewer FastAPI backend.
Contains all route definitions and API configuration.
"""

from .routes import api_router

__all__ = ["api_router"]
