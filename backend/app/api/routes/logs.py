"""
Log API Routes
=============

Handles log streaming and management endpoints
"""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
from typing import List, Optional
import asyncio
import json
import logging
from datetime import datetime

from app.models.schemas import (
    LogEntry, LogBatch, LogStreamResponse, ServiceRegistration,
    ProcessedLog, AnalyticsQuery, AnalyticsResponse
)
from app.services.log_processor import LogProcessorService
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency to get log processor service
async def get_log_processor():
    # This will be injected by the main app
    from main import log_processor
    return log_processor

@router.post("/stream/{service_name}", response_model=LogStreamResponse)
async def stream_logs(
    service_name: str,
    log_batch: LogBatch,
    background_tasks: BackgroundTasks,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """
    Stream logs from a microservice
    
    This endpoint receives batches of logs from microservices and queues them
    for processing. Processing happens asynchronously in the background.
    """
    try:
        # Validate service name
        if not service_name or len(service_name) > 100:
            raise HTTPException(status_code=400, detail="Invalid service name")
            
        # Validate batch
        if not log_batch.logs:
            raise HTTPException(status_code=400, detail="Empty log batch")
            
        if len(log_batch.logs) > settings.MAX_LOG_BATCH_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"Batch size exceeds maximum of {settings.MAX_LOG_BATCH_SIZE}"
            )
            
        # Register service if not already registered
        await processor.register_service(service_name)
        
        # Add logs to processing queue
        background_tasks.add_task(
            processor.add_log_batch, 
            service_name, 
            log_batch.logs
        )
        
        logger.info(f"Received {len(log_batch.logs)} logs from {service_name}")
        
        return LogStreamResponse(
            message=f"Successfully received {len(log_batch.logs)} logs",
            logs_received=len(log_batch.logs),
            processing_started=True,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing log stream from {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/stream/{service_name}/single", response_model=LogStreamResponse)
async def stream_single_log(
    service_name: str,
    log_entry: LogEntry,
    background_tasks: BackgroundTasks,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Stream a single log entry from a microservice"""
    try:
        # Create a batch with single log
        log_batch = LogBatch(
            service_name=service_name,
            logs=[log_entry]
        )
        
        return await stream_logs(service_name, log_batch, background_tasks, processor)
        
    except Exception as e:
        logger.error(f"Error processing single log from {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/services")
async def get_services(processor: LogProcessorService = Depends(get_log_processor)):
    """Get list of registered services"""
    try:
        services = await processor.get_registered_services()
        return {
            "services": services,
            "total_count": len(services),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting services: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/services/register", response_model=dict)
async def register_service(
    registration: ServiceRegistration,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Register a new service for log monitoring"""
    try:
        await processor.register_service(registration.service_name)
        
        logger.info(f"Manually registered service: {registration.service_name}")
        
        return {
            "message": f"Service {registration.service_name} registered successfully",
            "service_name": registration.service_name,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error registering service {registration.service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/services/{service_name}")
async def unregister_service(
    service_name: str,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Unregister a service"""
    try:
        await processor.unregister_service(service_name)
        
        logger.info(f"Unregistered service: {service_name}")
        
        return {
            "message": f"Service {service_name} unregistered successfully",
            "service_name": service_name,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error unregistering service {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/queue/status")
async def get_queue_status(processor: LogProcessorService = Depends(get_log_processor)):
    """Get current processing queue status"""
    try:
        stats = await processor.get_processing_stats()
        
        return {
            "queue_size": stats.queue_size,
            "processing_rate": stats.logs_per_second,
            "total_processed": stats.total_logs_processed,
            "processing_lag": stats.processing_lag,
            "last_processed": stats.last_processed_timestamp.isoformat(),
            "active_services": stats.active_services,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting queue status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/analyze", response_model=AnalyticsResponse)
async def analyze_logs(
    query: AnalyticsQuery,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """
    Analyze processed logs with filtering and aggregation
    
    This endpoint allows querying processed logs with various filters
    and returns aggregated statistics.
    """
    try:
        # TODO: Implement log analysis with database queries
        # For now, return mock data
        
        return AnalyticsResponse(
            total_count=0,
            results=[],
            aggregations={
                "services": {},
                "error_types": {},
                "severity_levels": {},
                "time_distribution": {}
            },
            query_time_ms=0.0,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error analyzing logs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/export/{service_name}")
async def export_logs(
    service_name: str,
    format: str = "json",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """Export logs for a service in various formats"""
    try:
        if format not in ["json", "csv", "txt"]:
            raise HTTPException(status_code=400, detail="Unsupported export format")
            
        # TODO: Implement log export functionality
        
        if format == "json":
            return {"message": "JSON export not yet implemented"}
        elif format == "csv":
            return {"message": "CSV export not yet implemented"}
        else:
            return {"message": "TXT export not yet implemented"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting logs for {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Streaming endpoint for continuous log ingestion
@router.post("/stream/{service_name}/continuous")
async def stream_logs_continuously(
    service_name: str,
    request: Request,
    processor: LogProcessorService = Depends(get_log_processor)
):
    """
    Continuous log streaming endpoint
    
    Accepts a stream of log entries separated by newlines.
    Each line should be a valid JSON log entry.
    """
    try:
        await processor.register_service(service_name)
        
        async def process_stream():
            buffer = ""
            logs_processed = 0
            
            async for chunk in request.stream():
                buffer += chunk.decode('utf-8')
                
                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if line:
                        try:
                            log_data = json.loads(line)
                            log_entry = LogEntry(**log_data)
                            
                            await processor.add_log_batch(service_name, [log_entry])
                            logs_processed += 1
                            
                        except (json.JSONDecodeError, ValueError) as e:
                            logger.warning(f"Invalid log line from {service_name}: {e}")
                            
            return logs_processed
            
        logs_count = await process_stream()
        
        return {
            "message": f"Processed {logs_count} logs from continuous stream",
            "service_name": service_name,
            "logs_processed": logs_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in continuous log stream from {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
