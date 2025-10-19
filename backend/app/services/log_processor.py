"""
Log Processor Service
====================

Handles continuous log processing in 30-second chunks
"""

import asyncio
import logging
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from collections import defaultdict, deque
import time

from app.models.schemas import (
    LogEntry, ProcessedLog, ServiceHealth, ProcessingStats, 
    ServiceStatus, LogBatch
)
from app.models.logsPreprocessor import (
    is_anomalous, extract_timestamp, extract_compact_error, 
    extract_anomaly_metadata
)
from app.models.logsClassifier import (
    classify_log_with_retry, get_preloaded_agent, 
    FallbackClassification
)
from app.core.config import settings

logger = logging.getLogger(__name__)

class LogProcessorService:
    """Service for continuous log processing"""
    
    def __init__(self):
        self.is_processing = False
        self.log_buffer: Dict[str, deque] = defaultdict(deque)
        self.service_health: Dict[str, ServiceHealth] = {}
        self.processing_stats = ProcessingStats(
            total_logs_processed=0,
            logs_per_second=0.0,
            active_services=0,
            total_anomalies=0,
            processing_lag=0.0,
            last_processed_timestamp=datetime.utcnow(),
            queue_size=0
        )
        self.registered_services: Set[str] = set()
        self.ai_agent = None
        self.last_processing_time = datetime.utcnow()
        
        # Processing metrics
        self.processed_logs_count = 0
        self.start_time = datetime.utcnow()
        
    async def start_continuous_processing(self):
        """Start the continuous log processing task"""
        logger.info("Starting continuous log processing...")
        self.is_processing = True
        
        # Initialize AI agent if enabled
        if settings.ENABLE_AI_CLASSIFICATION:
            try:
                self.ai_agent = get_preloaded_agent()
                logger.info("AI agent initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI agent: {e}")
                self.ai_agent = None
        
        # Start processing loop
        asyncio.create_task(self._processing_loop())
        
    async def stop_processing(self):
        """Stop the continuous processing"""
        logger.info("Stopping log processing...")
        self.is_processing = False
        
    def is_running(self) -> bool:
        """Check if processor is running"""
        return self.is_processing
        
    async def add_log_batch(self, service_name: str, logs: List[LogEntry]):
        """Add a batch of logs to the processing queue"""
        if not logs:
            return
            
        # Register service if not already registered
        self.registered_services.add(service_name)
        
        # Add logs to buffer
        for log in logs:
            self.log_buffer[service_name].append(log)
            
        # Update service health
        await self._update_service_health(service_name, logs)
        
        logger.debug(f"Added {len(logs)} logs from {service_name}")
        
    async def _processing_loop(self):
        """Main processing loop - runs every 30 seconds"""
        while self.is_processing:
            try:
                start_time = time.time()
                
                # Process logs for each service
                processed_count = 0
                anomaly_count = 0
                
                for service_name in list(self.registered_services):
                    service_processed, service_anomalies = await self._process_service_logs(service_name)
                    processed_count += service_processed
                    anomaly_count += service_anomalies
                
                # Update processing stats
                processing_time = time.time() - start_time
                self.processed_logs_count += processed_count
                
                self.processing_stats.total_logs_processed = self.processed_logs_count
                self.processing_stats.logs_per_second = processed_count / max(processing_time, 0.1)
                self.processing_stats.active_services = len(self.registered_services)
                self.processing_stats.total_anomalies += anomaly_count
                self.processing_stats.processing_lag = processing_time
                self.processing_stats.last_processed_timestamp = datetime.utcnow()
                self.processing_stats.queue_size = sum(len(queue) for queue in self.log_buffer.values())
                
                logger.info(f"Processed {processed_count} logs, {anomaly_count} anomalies in {processing_time:.2f}s")
                
                # Wait for next processing interval
                await asyncio.sleep(settings.LOG_PROCESSING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                await asyncio.sleep(5)  # Short sleep on error
                
    async def _process_service_logs(self, service_name: str) -> tuple[int, int]:
        """Process logs for a specific service"""
        if service_name not in self.log_buffer:
            return 0, 0
            
        logs_to_process = []
        processed_count = 0
        anomaly_count = 0
        
        # Get logs from buffer (up to max batch size)
        while (len(logs_to_process) < settings.MAX_LOG_BATCH_SIZE and 
               self.log_buffer[service_name]):
            logs_to_process.append(self.log_buffer[service_name].popleft())
            
        if not logs_to_process:
            return 0, 0
            
        # Process each log
        for log_entry in logs_to_process:
            try:
                processed_log = await self._process_single_log(log_entry)
                processed_count += 1
                
                if processed_log.is_anomaly:
                    anomaly_count += 1
                    # TODO: Store anomaly for further analysis
                    # TODO: Trigger alerts if needed
                    
            except Exception as e:
                logger.error(f"Error processing log from {service_name}: {e}")
                
        return processed_count, anomaly_count
        
    async def _process_single_log(self, log_entry: LogEntry) -> ProcessedLog:
        """Process a single log entry"""
        log_line = log_entry.message
        timestamp = log_entry.timestamp.isoformat()
        
        # Check if log is anomalous
        is_anomaly = is_anomalous(log_line)
        
        if is_anomaly and self.ai_agent:
            # Use AI classification for anomalies
            try:
                log_data = {
                    "line": log_line,
                    "timestamp": timestamp,
                    "service": log_entry.service_name
                }
                
                classification = classify_log_with_retry(log_data, agent=self.ai_agent)
                
                return ProcessedLog(
                    id=str(uuid.uuid4()),
                    original_log=log_entry,
                    service=classification.service,
                    error_type=classification.error_type,
                    error_sub_type=classification.error_sub_type,
                    error_desc=classification.error_desc,
                    severity_level=classification.severity_level,
                    timestamp=datetime.utcnow(),
                    is_anomaly=True,
                    confidence_score=0.8  # TODO: Get from AI model
                )
                
            except Exception as e:
                logger.error(f"AI classification failed: {e}")
                # Fall back to rule-based classification
                
        # Rule-based processing (fallback or non-anomalies)
        if is_anomaly:
            fallback = FallbackClassification.create_fallback({
                "line": log_line,
                "timestamp": timestamp,
                "service": log_entry.service_name
            }, timestamp)
            
            return ProcessedLog(
                id=str(uuid.uuid4()),
                original_log=log_entry,
                service=fallback.service,
                error_type=fallback.error_type,
                error_sub_type=fallback.error_sub_type,
                error_desc=fallback.error_desc,
                severity_level=fallback.severity_level,
                timestamp=datetime.utcnow(),
                is_anomaly=True,
                confidence_score=0.6
            )
        else:
            # Non-anomaly log
            from app.types.classifierTypes import ErrorType, ErrorSubtype, SeverityLevel
            
            return ProcessedLog(
                id=str(uuid.uuid4()),
                original_log=log_entry,
                service=log_entry.service_name,
                error_type=ErrorType.UNKNOWN_ERROR,
                error_sub_type=ErrorSubtype.UNKNOWN,
                error_desc="Normal log entry",
                severity_level=SeverityLevel.LOW,
                timestamp=datetime.utcnow(),
                is_anomaly=False,
                confidence_score=0.9
            )
            
    async def _update_service_health(self, service_name: str, logs: List[LogEntry]):
        """Update health status for a service"""
        current_time = datetime.utcnow()
        
        # Calculate error metrics
        total_logs = len(logs)
        error_logs = sum(1 for log in logs if log.level in ["ERROR", "FATAL"])
        warning_logs = sum(1 for log in logs if log.level == "WARN")
        
        error_rate = error_logs / max(total_logs, 1)
        
        # Determine status
        if error_rate > 0.1:  # 10% error rate
            status = ServiceStatus.CRITICAL
        elif error_rate > 0.05 or warning_logs > 0:  # 5% error rate or warnings
            status = ServiceStatus.WARNING
        else:
            status = ServiceStatus.HEALTHY
            
        # Update or create health record
        if service_name in self.service_health:
            health = self.service_health[service_name]
            health.last_seen = current_time
            health.error_rate = error_rate
            health.total_logs += total_logs
            health.error_count += error_logs
            health.warning_count += warning_logs
            health.status = status
        else:
            self.service_health[service_name] = ServiceHealth(
                service_name=service_name,
                status=status,
                last_seen=current_time,
                error_rate=error_rate,
                total_logs=total_logs,
                error_count=error_logs,
                warning_count=warning_logs,
                severity_breakdown={
                    "High": error_logs,
                    "Medium": warning_logs,
                    "Low": total_logs - error_logs - warning_logs
                },
                most_common_errors=[],
                uptime_percentage=95.0  # TODO: Calculate actual uptime
            )
            
    async def get_service_health(self, service_name: Optional[str] = None) -> Dict[str, ServiceHealth]:
        """Get health status for services"""
        if service_name:
            return {service_name: self.service_health.get(service_name)}
        return self.service_health.copy()
        
    async def get_processing_stats(self) -> ProcessingStats:
        """Get current processing statistics"""
        return self.processing_stats
        
    async def get_registered_services(self) -> List[str]:
        """Get list of registered services"""
        return list(self.registered_services)
        
    async def register_service(self, service_name: str):
        """Register a new service"""
        self.registered_services.add(service_name)
        logger.info(f"Registered service: {service_name}")
        
    async def unregister_service(self, service_name: str):
        """Unregister a service"""
        self.registered_services.discard(service_name)
        if service_name in self.log_buffer:
            del self.log_buffer[service_name]
        if service_name in self.service_health:
            del self.service_health[service_name]
        logger.info(f"Unregistered service: {service_name}")
