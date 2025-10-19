"""
Health Monitoring API Routes
===========================

Provides health status and monitoring endpoints for all microservices
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict
import logging
from datetime import datetime, timedelta

from app.models.schemas import (
    ServiceHealth, SystemHealth, HealthAlert, 
    HealthQuery, HealthResponse, AlertConfiguration
)
from app.services.log_processor import LogProcessorService

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency to get log processor service
async def get_log_processor():
    # This will be injected by the main app
    from main import log_processor
    return log_processor

@router.get("/", response_model=SystemHealth)
async def get_system_health(processor: LogProcessorService = Depends(get_log_processor)):
    """Get overall system health status"""
    try:
        # Get health for all services
        services_health = await processor.get_all_services_health()
        
        # Calculate overall system status
        overall_status = "healthy"
        critical_count = sum(1 for health in services_health if health.status == "critical")
        warning_count = sum(1 for health in services_health if health.status == "warning")
        
        if critical_count > 0:
            overall_status = "critical"
        elif warning_count > 0:
            overall_status = "warning"
            
        return SystemHealth(
            overall_status=overall_status,
            services=services_health,
            total_services=len(services_health),
            healthy_services=sum(1 for h in services_health if h.status == "healthy"),
            warning_services=warning_count,
            critical_services=critical_count,
            last_updated=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/services/{service_name}", response_model=ServiceHealth)
async def get_service_health(
    service_name: str,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Get detailed health status for a specific service"""
    try:
        health = await processor.get_service_health(service_name)
        
        if not health:
            raise HTTPException(
                status_code=404, 
                detail=f"Service {service_name} not found"
            )
            
        return health
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting health for service {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/services", response_model=List[ServiceHealth])
async def get_all_services_health(processor: LogProcessorService = Depends(get_log_processor)):
    """Get health status for all registered services"""
    try:
        return await processor.get_all_services_health()
        
    except Exception as e:
        logger.error(f"Error getting all services health: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/query", response_model=HealthResponse)
async def query_health_data(
    query: HealthQuery,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Query health data with filters and time ranges"""
    try:
        # TODO: Implement health data querying with database
        # For now, return current health data
        
        if query.service_name:
            health = await processor.get_service_health(query.service_name)
            services_health = [health] if health else []
        else:
            services_health = await processor.get_all_services_health()
            
        # Filter by status if specified
        if query.status_filter:
            services_health = [
                h for h in services_health 
                if h.status in query.status_filter
            ]
            
        return HealthResponse(
            services=services_health,
            total_count=len(services_health),
            query_timestamp=datetime.utcnow(),
            filters_applied={
                "service_name": query.service_name,
                "status_filter": query.status_filter,
                "time_range": {
                    "start": query.start_time.isoformat() if query.start_time else None,
                    "end": query.end_time.isoformat() if query.end_time else None
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error querying health data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/alerts", response_model=List[HealthAlert])
async def get_active_alerts(processor: LogProcessorService = Depends(get_log_processor)):
    """Get all active health alerts"""
    try:
        alerts = await processor.get_active_alerts()
        return alerts
        
    except Exception as e:
        logger.error(f"Error getting active alerts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/alerts/{service_name}", response_model=List[HealthAlert])
async def get_service_alerts(
    service_name: str,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Get active alerts for a specific service"""
    try:
        alerts = await processor.get_service_alerts(service_name)
        return alerts
        
    except Exception as e:
        logger.error(f"Error getting alerts for service {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Acknowledge a health alert"""
    try:
        success = await processor.acknowledge_alert(alert_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
            
        return {
            "message": f"Alert {alert_id} acknowledged successfully",
            "alert_id": alert_id,
            "acknowledged_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error acknowledging alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/alerts/{alert_id}")
async def dismiss_alert(
    alert_id: str,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Dismiss a health alert"""
    try:
        success = await processor.dismiss_alert(alert_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
            
        return {
            "message": f"Alert {alert_id} dismissed successfully",
            "alert_id": alert_id,
            "dismissed_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error dismissing alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/metrics/{service_name}")
async def get_service_metrics(
    service_name: str,
    hours: int = 24,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Get detailed metrics for a service over time"""
    try:
        if hours < 1 or hours > 168:  # Max 7 days
            raise HTTPException(
                status_code=400, 
                detail="Hours must be between 1 and 168"
            )
            
        # TODO: Implement metrics retrieval from database
        # For now, return mock data structure
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        return {
            "service_name": service_name,
            "time_range": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "hours": hours
            },
            "metrics": {
                "error_rate": {
                    "current": 0.0,
                    "average": 0.0,
                    "trend": "stable"
                },
                "response_time": {
                    "current": 0.0,
                    "average": 0.0,
                    "p95": 0.0,
                    "p99": 0.0
                },
                "throughput": {
                    "current": 0.0,
                    "average": 0.0,
                    "peak": 0.0
                },
                "availability": {
                    "current": 100.0,
                    "average": 100.0,
                    "uptime_percentage": 100.0
                }
            },
            "time_series": [],  # Will contain time-series data
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metrics for service {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/trends")
async def get_health_trends(
    hours: int = 24,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Get system-wide health trends"""
    try:
        if hours < 1 or hours > 168:  # Max 7 days
            raise HTTPException(
                status_code=400, 
                detail="Hours must be between 1 and 168"
            )
            
        # TODO: Implement trend analysis
        # For now, return mock structure
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        return {
            "time_range": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "hours": hours
            },
            "system_trends": {
                "overall_health_score": 95.0,
                "trend_direction": "stable",
                "incident_count": 0,
                "resolution_time_avg": 0.0
            },
            "service_trends": {},  # Per-service trend data
            "predictions": {
                "next_24h_health_score": 95.0,
                "risk_level": "low",
                "recommendations": []
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting health trends: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/alerts/config", response_model=dict)
async def configure_alerts(
    config: AlertConfiguration,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Configure alert thresholds and rules"""
    try:
        # TODO: Implement alert configuration
        await processor.configure_alerts(config)
        
        return {
            "message": "Alert configuration updated successfully",
            "service_name": config.service_name,
            "configuration": config.dict(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error configuring alerts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
