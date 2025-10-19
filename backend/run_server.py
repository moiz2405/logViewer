"""
FastAPI Backend Startup Script
=============================

Run this script to start the LogViewer FastAPI backend server.
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    """Start the FastAPI server"""
    print("🚀 Starting LogViewer FastAPI Backend...")
    print(f"📁 Backend directory: {backend_dir}")
    print("📡 Server will be available at: http://localhost:8000")
    print("📋 API documentation will be available at: http://localhost:8000/docs")
    print("🔄 WebSocket endpoints will be available at: ws://localhost:8000/api/ws/")
    print()
    
    try:
        # Start the FastAPI server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,  # Enable auto-reload during development
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
