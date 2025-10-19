"""
API Routes Package
=================

This package contains all the API route definitions for the LogViewer FastAPI backend.

Routes are organized by functionality:
- logs: Log streaming and management endpoints
- health: Health monitoring and status endpoints  
- analytics: Analytics and insights endpoints
- notifications: Notification management endpoints
- websockets: Real-time WebSocket endpoints

All routes are included in the main FastAPI application through this package.
"""

from fastapi import APIRouter
from .logs import router as logs_router
from .health import router as health_router
from .analytics import router as analytics_router
from .notifications import router as notifications_router
from .websockets import router as websockets_router

# Create main API router
api_router = APIRouter()

# Include all route modules with appropriate prefixes
api_router.include_router(
    logs_router,
    prefix="/logs",
    tags=["logs"],
    responses={404: {"description": "Not found"}}
)

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}}
)

api_router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}}
)

api_router.include_router(
    notifications_router,
    prefix="/notifications",
    tags=["notifications"],
    responses={404: {"description": "Not found"}}
)

api_router.include_router(
    websockets_router,
    prefix="/ws",
    tags=["websockets"],
    responses={404: {"description": "Not found"}}
)

# Root endpoint for API health check
@api_router.get("/")
async def api_root():
    """API root endpoint - health check for the API itself"""
    return {
        "message": "LogViewer FastAPI Backend",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "logs": "/api/logs",
            "health": "/api/health", 
            "analytics": "/api/analytics",
            "notifications": "/api/notifications",
            "websockets": "/api/ws"
        },
        "documentation": "/docs"
    }

# API status endpoint
@api_router.get("/status")
async def api_status():
    """Get API status and basic information"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "features": {
            "log_streaming": True,
            "real_time_health": True,
            "ai_analytics": True,
            "notifications": True,
            "websockets": True
        },
        "limits": {
            "max_log_batch_size": 1000,
            "max_websocket_connections": 100,
            "rate_limit_per_minute": 1000
        }
    }
