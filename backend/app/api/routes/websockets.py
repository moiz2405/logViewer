"""
WebSocket API Routes
===================

Handles real-time WebSocket connections for live updates
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Optional, Dict, Any
import json
import logging
from datetime import datetime

from app.models.schemas import (
    WebSocketMessage, WebSocketResponse, SubscriptionRequest,
    WebSocketConnectionInfo
)
from app.services.websocket_manager import WebSocketManager
from app.services.log_processor import LogProcessorService

logger = logging.getLogger(__name__)
router = APIRouter()

# Global WebSocket manager instance
websocket_manager = WebSocketManager()

# Dependency to get log processor service
async def get_log_processor():
    # This will be injected by the main app
    from main import log_processor
    return log_processor

@router.websocket("/live")
async def websocket_live_updates(
    websocket: WebSocket,
    service: Optional[str] = None,
    client_id: Optional[str] = None
):
    """
    Main WebSocket endpoint for live updates
    
    Supports:
    - Real-time log streaming
    - Health status updates
    - Alert notifications
    - System metrics
    """
    await websocket.accept()
    
    # Generate client ID if not provided
    if not client_id:
        client_id = f"client_{datetime.utcnow().timestamp()}"
    
    # Add connection to manager
    await websocket_manager.connect(websocket, client_id, service)
    
    # Send welcome message
    welcome_message = WebSocketResponse(
        type="connection",
        data={
            "status": "connected",
            "client_id": client_id,
            "service_filter": service,
            "timestamp": datetime.utcnow().isoformat()
        },
        timestamp=datetime.utcnow()
    )
    
    await websocket.send_text(welcome_message.json())
    
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            
            try:
                # Parse incoming message
                message = json.loads(data)
                await handle_websocket_message(websocket, client_id, message)
                
            except json.JSONDecodeError:
                # Send error response
                error_response = WebSocketResponse(
                    type="error",
                    data={"error": "Invalid JSON format"},
                    timestamp=datetime.utcnow()
                )
                await websocket.send_text(error_response.json())
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket client {client_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
    finally:
        # Clean up connection
        websocket_manager.disconnect(client_id)

@router.websocket("/health")
async def websocket_health_updates(
    websocket: WebSocket,
    service: Optional[str] = None,
    client_id: Optional[str] = None
):
    """
    WebSocket endpoint specifically for health status updates
    """
    await websocket.accept()
    
    if not client_id:
        client_id = f"health_client_{datetime.utcnow().timestamp()}"
    
    # Add to health-specific connection pool
    await websocket_manager.connect(websocket, client_id, service, connection_type="health")
    
    try:
        # Send initial health status
        # TODO: Get current health status from processor
        initial_health = {
            "type": "health_status",
            "service": service,
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await websocket.send_text(json.dumps(initial_health))
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Handle health-specific messages if needed
            
    except WebSocketDisconnect:
        logger.info(f"Health WebSocket client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Health WebSocket error for client {client_id}: {e}")
    finally:
        websocket_manager.disconnect(client_id)

@router.websocket("/logs/{service_name}")
async def websocket_service_logs(
    websocket: WebSocket,
    service_name: str,
    client_id: Optional[str] = None
):
    """
    WebSocket endpoint for service-specific log streaming
    """
    await websocket.accept()
    
    if not client_id:
        client_id = f"logs_client_{datetime.utcnow().timestamp()}"
    
    # Connect with service-specific filter
    await websocket_manager.connect(websocket, client_id, service_name, connection_type="logs")
    
    try:
        # Send connection confirmation
        confirmation = {
            "type": "service_logs_connection",
            "service": service_name,
            "status": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await websocket.send_text(json.dumps(confirmation))
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle log filtering requests
            if message.get("type") == "filter":
                await handle_log_filter_request(websocket, client_id, message)
            elif message.get("type") == "subscription":
                await handle_subscription_request(websocket, client_id, message)
                
    except WebSocketDisconnect:
        logger.info(f"Service logs WebSocket client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Service logs WebSocket error for client {client_id}: {e}")
    finally:
        websocket_manager.disconnect(client_id)

@router.websocket("/alerts")
async def websocket_alerts(
    websocket: WebSocket,
    client_id: Optional[str] = None
):
    """
    WebSocket endpoint specifically for alert notifications
    """
    await websocket.accept()
    
    if not client_id:
        client_id = f"alerts_client_{datetime.utcnow().timestamp()}"
    
    await websocket_manager.connect(websocket, client_id, connection_type="alerts")
    
    try:
        # Send connection confirmation
        confirmation = {
            "type": "alerts_connection",
            "status": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await websocket.send_text(json.dumps(confirmation))
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle alert acknowledgments
            if message.get("type") == "acknowledge":
                await handle_alert_acknowledgment(websocket, client_id, message)
                
    except WebSocketDisconnect:
        logger.info(f"Alerts WebSocket client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Alerts WebSocket error for client {client_id}: {e}")
    finally:
        websocket_manager.disconnect(client_id)

# Message handlers
async def handle_websocket_message(websocket: WebSocket, client_id: str, message: Dict[str, Any]):
    """Handle incoming WebSocket messages"""
    try:
        message_type = message.get("type")
        
        if message_type == "ping":
            # Respond to ping with pong
            pong_response = WebSocketResponse(
                type="pong",
                data={"timestamp": datetime.utcnow().isoformat()},
                timestamp=datetime.utcnow()
            )
            await websocket.send_text(pong_response.json())
            
        elif message_type == "subscribe":
            # Handle subscription request
            await handle_subscription_request(websocket, client_id, message)
            
        elif message_type == "unsubscribe":
            # Handle unsubscription request
            await handle_unsubscription_request(websocket, client_id, message)
            
        elif message_type == "filter":
            # Handle filter update
            await handle_filter_update(websocket, client_id, message)
            
        else:
            # Unknown message type
            error_response = WebSocketResponse(
                type="error",
                data={"error": f"Unknown message type: {message_type}"},
                timestamp=datetime.utcnow()
            )
            await websocket.send_text(error_response.json())
            
    except Exception as e:
        logger.error(f"Error handling WebSocket message from {client_id}: {e}")
        
        error_response = WebSocketResponse(
            type="error",
            data={"error": "Message processing failed"},
            timestamp=datetime.utcnow()
        )
        await websocket.send_text(error_response.json())

async def handle_subscription_request(websocket: WebSocket, client_id: str, message: Dict[str, Any]):
    """Handle subscription requests"""
    try:
        subscription_type = message.get("subscription_type")
        service_name = message.get("service_name")
        filters = message.get("filters", {})
        
        # Update client subscription in manager
        await websocket_manager.update_subscription(client_id, subscription_type, service_name, filters)
        
        # Send confirmation
        response = WebSocketResponse(
            type="subscription_confirmed",
            data={
                "subscription_type": subscription_type,
                "service_name": service_name,
                "filters": filters
            },
            timestamp=datetime.utcnow()
        )
        await websocket.send_text(response.json())
        
    except Exception as e:
        logger.error(f"Error handling subscription request from {client_id}: {e}")

async def handle_unsubscription_request(websocket: WebSocket, client_id: str, message: Dict[str, Any]):
    """Handle unsubscription requests"""
    try:
        subscription_type = message.get("subscription_type")
        
        # Remove subscription in manager
        await websocket_manager.remove_subscription(client_id, subscription_type)
        
        # Send confirmation
        response = WebSocketResponse(
            type="unsubscription_confirmed",
            data={"subscription_type": subscription_type},
            timestamp=datetime.utcnow()
        )
        await websocket.send_text(response.json())
        
    except Exception as e:
        logger.error(f"Error handling unsubscription request from {client_id}: {e}")

async def handle_filter_update(websocket: WebSocket, client_id: str, message: Dict[str, Any]):
    """Handle filter update requests"""
    try:
        filters = message.get("filters", {})
        
        # Update filters in manager
        await websocket_manager.update_filters(client_id, filters)
        
        # Send confirmation
        response = WebSocketResponse(
            type="filters_updated",
            data={"filters": filters},
            timestamp=datetime.utcnow()
        )
        await websocket.send_text(response.json())
        
    except Exception as e:
        logger.error(f"Error handling filter update from {client_id}: {e}")

async def handle_log_filter_request(websocket: WebSocket, client_id: str, message: Dict[str, Any]):
    """Handle log-specific filter requests"""
    try:
        log_level = message.get("log_level")
        keywords = message.get("keywords", [])
        time_range = message.get("time_range")
        
        # Update log filters in manager
        filters = {
            "log_level": log_level,
            "keywords": keywords,
            "time_range": time_range
        }
        
        await websocket_manager.update_filters(client_id, filters)
        
        # Send confirmation
        response = {
            "type": "log_filters_updated",
            "filters": filters,
            "timestamp": datetime.utcnow().isoformat()
        }
        await websocket.send_text(json.dumps(response))
        
    except Exception as e:
        logger.error(f"Error handling log filter request from {client_id}: {e}")

async def handle_alert_acknowledgment(websocket: WebSocket, client_id: str, message: Dict[str, Any]):
    """Handle alert acknowledgment"""
    try:
        alert_id = message.get("alert_id")
        
        # TODO: Process alert acknowledgment
        # This would typically update the alert status in the database
        
        # Send confirmation
        response = {
            "type": "alert_acknowledged",
            "alert_id": alert_id,
            "acknowledged_by": client_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await websocket.send_text(json.dumps(response))
        
        # Broadcast acknowledgment to other clients
        await websocket_manager.broadcast_to_type("alerts", response)
        
    except Exception as e:
        logger.error(f"Error handling alert acknowledgment from {client_id}: {e}")

# Utility functions for the WebSocket manager to use
async def get_websocket_manager():
    """Get the WebSocket manager instance"""
    return websocket_manager

@router.get("/connections")
async def get_active_connections():
    """Get information about active WebSocket connections"""
    try:
        connections = websocket_manager.get_connection_info()
        
        return {
            "total_connections": len(connections),
            "connections_by_type": websocket_manager.get_connections_by_type(),
            "connections": [
                {
                    "client_id": conn.client_id,
                    "service_filter": conn.service_filter,
                    "connection_type": conn.connection_type,
                    "connected_at": conn.connected_at.isoformat(),
                    "last_activity": conn.last_activity.isoformat()
                }
                for conn in connections
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting connection info: {e}")
        return {
            "error": "Unable to get connection information",
            "timestamp": datetime.utcnow().isoformat()
        }
