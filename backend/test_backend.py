"""
Simple FastAPI Backend Test
==========================

Basic test to verify the FastAPI backend structure works.
Run this to test the backend without all dependencies.
"""

try:
    import sys
    from pathlib import Path
    
    # Add backend to path
    backend_dir = Path(__file__).parent
    sys.path.insert(0, str(backend_dir))
    
    print("✅ Python path configured")
    
    # Test basic imports
    try:
        from app.core.config import Settings
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        
    try:
        from app.models.schemas import LogEntry
        print("✅ Schemas module imported successfully") 
    except ImportError as e:
        print(f"❌ Schemas import failed: {e}")
        
    try:
        from app.services.log_processor import LogProcessorService
        print("✅ Log processor service imported successfully")
    except ImportError as e:
        print(f"❌ Log processor import failed: {e}")
        
    try:
        from app.services.websocket_manager import WebSocketManager
        print("✅ WebSocket manager imported successfully")
    except ImportError as e:
        print(f"❌ WebSocket manager import failed: {e}")
        
    # Test existing models
    try:
        sys.path.append(str(backend_dir / "app"))
        from models.logsClassifier import LogsClassifier
        print("✅ Existing LogsClassifier imported successfully")
    except ImportError as e:
        print(f"❌ LogsClassifier import failed: {e}")
        
    try:
        from models.logsPreprocessor import LogsPreprocessor  
        print("✅ Existing LogsPreprocessor imported successfully")
    except ImportError as e:
        print(f"❌ LogsPreprocessor import failed: {e}")
        
    print("\n🏗️  Backend structure verification complete!")
    print("📝 Note: Install FastAPI dependencies to run the full server")
    print("💡 Use: pip install fastapi uvicorn websockets")
    
except Exception as e:
    print(f"❌ Backend test failed: {e}")
    import traceback
    traceback.print_exc()
