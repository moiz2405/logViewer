"""
WebSocket Manager
================

Handles real-time WebSocket connections for live updates
"""

import asyncio
import json
import logging
from typing import Dict, List, Set
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect
from app.models.schemas import ServiceHealth, ProcessingStats
from app.core.config import settings

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for a service"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.active_connections: List[WebSocket] = []
        self.last_heartbeat = datetime.utcnow()
        
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection for {self.service_name}. Total: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket disconnected from {self.service_name}. Total: {len(self.active_connections)}")
            
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")
            self.disconnect(websocket)
            
    async def broadcast(self, message: str):
        """Broadcast a message to all connected WebSockets"""
        if not self.active_connections:
            return
            
        # Send to all connections, remove dead ones
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                dead_connections.append(connection)
                
        # Clean up dead connections
        for dead_conn in dead_connections:
            self.disconnect(dead_conn)
            
    def is_active(self) -> bool:
        """Check if there are any active connections"""
        return len(self.active_connections) > 0
        
    def connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)

class WebSocketManager:
    """Main WebSocket manager"""
    
    def __init__(self):
        self.service_managers: Dict[str, ConnectionManager] = {}
        self.global_connections: List[WebSocket] = []
        self.is_initialized = False
        self.heartbeat_task = None
        
    async def initialize(self):
        """Initialize the WebSocket manager"""
        logger.info("Initializing WebSocket manager...")
        self.is_initialized = True
        
        # Start heartbeat task
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
    async def cleanup(self):
        """Cleanup WebSocket manager"""
        logger.info("Cleaning up WebSocket manager...")
        self.is_initialized = False
        
        # Cancel heartbeat task
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            
        # Close all connections
        for manager in self.service_managers.values():
            for connection in manager.active_connections:
                try:
                    await connection.close()
                except:
                    pass
                    
        for connection in self.global_connections:
            try:
                await connection.close()
            except:
                pass
                
    async def connect(self, websocket: WebSocket, service_name: str):
        """Connect a WebSocket to a specific service"""
        if service_name == "global":
            # Global connection for all services
            await websocket.accept()
            self.global_connections.append(websocket)
            logger.info(f"New global WebSocket connection. Total: {len(self.global_connections)}")
        else:
            # Service-specific connection
            if service_name not in self.service_managers:
                self.service_managers[service_name] = ConnectionManager(service_name)
                
            await self.service_managers[service_name].connect(websocket)
            
    def disconnect(self, websocket: WebSocket, service_name: str):
        """Disconnect a WebSocket"""
        if service_name == "global":
            if websocket in self.global_connections:
                self.global_connections.remove(websocket)
                logger.info(f"Global WebSocket disconnected. Total: {len(self.global_connections)}")
        else:
            if service_name in self.service_managers:
                self.service_managers[service_name].disconnect(websocket)
                
                # Remove manager if no connections
                if not self.service_managers[service_name].is_active():
                    del self.service_managers[service_name]
                    
    async def send_to_service(self, service_name: str, message: Dict):
        """Send a message to all connections for a specific service"""
        if service_name in self.service_managers:
            message_str = json.dumps(message)
            await self.service_managers[service_name].broadcast(message_str)
            
    async def broadcast_global(self, message: Dict):
        """Broadcast a message to all global connections"""
        if not self.global_connections:
            return
            
        message_str = json.dumps(message)
        dead_connections = []
        
        for connection in self.global_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Error broadcasting to global WebSocket: {e}")
                dead_connections.append(connection)
                
        # Clean up dead connections
        for dead_conn in dead_connections:
            if dead_conn in self.global_connections:
                self.global_connections.remove(dead_conn)
                
    async def broadcast_health_update(self, service_name: str, health: ServiceHealth):
        """Broadcast a health update for a service"""
        message = {
            "type": "health_update",
            "service_name": service_name,
            "data": health.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send to service-specific connections
        await self.send_to_service(service_name, message)
        
        # Send to global connections
        await self.broadcast_global(message)
        
    async def broadcast_stats_update(self, stats: ProcessingStats):
        """Broadcast processing statistics update"""
        message = {
            "type": "stats_update",
            "data": stats.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast_global(message)
        
    async def broadcast_anomaly_alert(self, service_name: str, anomaly_data: Dict):
        """Broadcast an anomaly alert"""
        message = {
            "type": "anomaly_alert",
            "service_name": service_name,
            "data": anomaly_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send to service-specific connections
        await self.send_to_service(service_name, message)
        
        # Send to global connections
        await self.broadcast_global(message)
        
    async def handle_message(self, service_name: str, data: str):
        """Handle incoming WebSocket message"""
        try:
            message = json.loads(data)
            message_type = message.get("type")
            
            if message_type == "ping":
                # Respond to ping with pong
                pong_message = {
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                }
                await self.send_to_service(service_name, pong_message)
                
            elif message_type == "subscribe":
                # Handle subscription requests
                # TODO: Implement subscription logic
                pass
                
            elif message_type == "get_health":
                # TODO: Send current health status
                pass
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from {service_name}: {data}")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
            
    async def _heartbeat_loop(self):
        """Send periodic heartbeat to maintain connections"""
        while self.is_initialized:
            try:
                heartbeat_message = {
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat(),
                    "active_services": len(self.service_managers),
                    "total_connections": self.get_total_connections()
                }
                
                await self.broadcast_global(heartbeat_message)
                
                # Wait for next heartbeat
                await asyncio.sleep(settings.WEBSOCKET_KEEPALIVE_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in heartbeat loop: {e}")
                await asyncio.sleep(5)
                
    def is_active(self) -> bool:
        """Check if WebSocket manager is active"""
        return self.is_initialized
        
    def get_total_connections(self) -> int:
        """Get total number of active connections"""
        service_connections = sum(
            manager.connection_count() 
            for manager in self.service_managers.values()
        )
        return len(self.global_connections) + service_connections
        
    def get_service_connections(self, service_name: str) -> int:
        """Get number of connections for a specific service"""
        if service_name in self.service_managers:
            return self.service_managers[service_name].connection_count()
        return 0
        
    def get_connection_stats(self) -> Dict[str, int]:
        """Get connection statistics"""
        stats = {
            "global_connections": len(self.global_connections),
            "total_connections": self.get_total_connections(),
            "active_services": len(self.service_managers)
        }
        
        # Add per-service stats
        for service_name, manager in self.service_managers.items():
            stats[f"service_{service_name}"] = manager.connection_count()
            
        return stats
