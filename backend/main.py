"""
LogViewer FastAPI Backend
========================

A streaming log analysis system that receives logs from microservices,
processes them in real-time, and provides health monitoring dashboard.

Features:
- Continuous log streaming endpoints
- Real-time log processing in 30-second chunks
- Health monitoring for microservices
- AI-powered classification and analysis
- WebSocket support for real-time updates
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json

from app.core.config import Settings
from app.api.routes import logs, health, analytics, notifications
from app.services.log_processor import LogProcessorService
from app.services.websocket_manager import WebSocketManager
from app.models.schemas import LogEntry, ServiceHealth, ProcessingStats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LogViewer API",
    description="Intelligent Log Analysis & Classification System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Settings
settings = Settings()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
log_processor = LogProcessorService()
websocket_manager = WebSocketManager()

# Include API routes
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting LogViewer API...")
    
    # Start background log processing task
    asyncio.create_task(log_processor.start_continuous_processing())
    
    # Initialize websocket manager
    await websocket_manager.initialize()
    
    logger.info("LogViewer API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down LogViewer API...")
    await log_processor.stop_processing()
    await websocket_manager.cleanup()
    logger.info("LogViewer API shut down complete")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "LogViewer API is running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "log_processor": log_processor.is_running(),
            "websocket_manager": websocket_manager.is_active(),
        }
    }

@app.websocket("/ws/{service_name}")
async def websocket_endpoint(websocket: WebSocket, service_name: str):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket, service_name)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            await websocket_manager.handle_message(service_name, data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, service_name)

@app.get("/api/v1/services")
async def get_registered_services():
    """Get list of all registered services"""
    services = await log_processor.get_registered_services()
    return {
        "services": services,
        "total_count": len(services),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/stats")
async def get_processing_stats():
    """Get real-time processing statistics"""
    stats = await log_processor.get_processing_stats()
    return {
        "stats": stats,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
