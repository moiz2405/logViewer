from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import os
import time
import requests
import json
from typing import Dict, List, Optional
from threading import Thread, Event

# Import log processor
from backend.app.models.smart_log_processor import (
    process_and_summarize_logs,
    process_and_summarize_stream,
)

app = FastAPI(title="Smart Log Processor API")

# =========================================
# Globals
# =========================================
MAX_QUEUE_SIZE = 1000
log_queues: Dict[str, asyncio.Queue] = {}
queue_last_activity: Dict[str, float] = {}
stop_flags: Dict[str, Event] = {}  # to stop background processors

# =========================================
# Schemas
# =========================================
class LogProcessRequest(BaseModel):
    app_id: str
    app_name: str
    log_url: Optional[str] = None
    log_lines: Optional[List[str]] = None


# =========================================
# Streaming Endpoint
# =========================================
@app.get("/stream/{app_id}")
async def stream_logs(app_id: str):
    """Stream live logs via Server-Sent Events"""
    if app_id not in log_queues:
        log_queues[app_id] = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)

    async def event_stream():
        while True:
            log_entry = await log_queues[app_id].get()
            yield f"data: {log_entry['log']}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# =========================================
# One-Time Log Processing
# =========================================
@app.post("/process-log")
async def process_log(request: LogProcessRequest):
    """Accepts logs via URL or inline array and processes them once."""
    app_id = request.app_id
    app_name = request.app_name

    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs", app_id)
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    local_log_path = os.path.join(logs_dir, f"{app_id}.log")

    # Gather logs
    if request.log_url:
        resp = requests.get(request.log_url)
        resp.raise_for_status()
        log_lines = resp.text.splitlines()
    elif request.log_lines:
        log_lines = request.log_lines
    else:
        return {"error": "Either log_url or log_lines must be provided"}

    # Stream logs to connected clients
    if app_id not in log_queues:
        log_queues[app_id] = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)
    for line in log_lines:
        queue_last_activity[app_id] = time.time()
        try:
            log_queues[app_id].put_nowait({"app_id": app_id, "app_name": app_name, "log": line})
        except asyncio.QueueFull:
            print(f"Queue full for {app_id}, dropping log.")

    # Save locally
    with open(local_log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    # Process & summarize
    dashboard = process_and_summarize_stream(log_lines, outputs_dir)

    return {
        "status": "success",
        "app_id": app_id,
        "app_name": app_name,
        "dashboard_summary": dashboard,
    }


# =========================================
# Continuous Log Processing (Background)
# =========================================
def continuous_processor(app_id: str, app_name: str, log_url: str, batch_duration=20, sleep_interval=10):
    print(f"[{app_id}] Continuous processor started...")
    stop_flags[app_id] = Event()
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs", app_id)
    os.makedirs(outputs_dir, exist_ok=True)

    collected_logs = []
    start_time = time.time()

    try:
        with requests.get(log_url, stream=True) as response:
            for line in response.iter_lines():
                if stop_flags[app_id].is_set():
                    print(f"[{app_id}] Stop signal received. Exiting loop.")
                    break

                if not line or not line.startswith(b"data:"):
                    continue
                log_line = line.decode().replace("data: ", "").strip()
                collected_logs.append(log_line)

                # Process every batch_duration seconds
                if time.time() - start_time >= batch_duration:
                    print(f"[{app_id}] Processing {len(collected_logs)} logs...")
                    process_and_summarize_stream(collected_logs, outputs_dir)
                    collected_logs = []
                    start_time = time.time()
                    time.sleep(sleep_interval)

    except Exception as e:
        print(f"[{app_id}] Continuous processor error: {e}")

    print(f"[{app_id}] Continuous processor stopped.")


@app.post("/start-continuous")
def start_continuous_processing(request: LogProcessRequest):
    """Starts continuous streaming + processing of logs from a URL."""
    if not request.log_url:
        return {"error": "log_url required for continuous processing"}

    app_id = request.app_id
    app_name = request.app_name
    if app_id in stop_flags and not stop_flags[app_id].is_set():
        return {"status": "already_running"}

    thread = Thread(
        target=continuous_processor,
        args=(app_id, app_name, request.log_url),
        daemon=True,
    )
    thread.start()
    return {"status": "started", "app_id": app_id}


@app.post("/stop-process/{app_id}")
def stop_continuous_processing(app_id: str):
    """Stop a running continuous processor."""
    if app_id not in stop_flags:
        return {"status": "not_running"}
    stop_flags[app_id].set()
    return {"status": "stopping", "app_id": app_id}

# =========================================
# Continuous Summary Streaming via SSE
# =========================================
@app.get("/continuous-summary/{app_id}")
async def continuous_summary(app_id: str, log_url: str, batch_duration: int = 20, idle_gap: int = 10):
    """
    Streams processed dashboard summaries every batch_duration seconds
    from the provided log_url (SSE or raw text endpoint).
    """
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs", app_id)
    os.makedirs(outputs_dir, exist_ok=True)

    async def event_stream():
        collected_logs = []
        start_time = time.time()

        try:
            with requests.get(log_url, stream=True) as response:
                for line in response.iter_lines():
                    if not line or not line.startswith(b"data:"):
                        continue

                    log_line = line.decode().replace("data: ", "").strip()
                    collected_logs.append(log_line)

                    # Process logs every batch_duration seconds
                    if time.time() - start_time >= batch_duration:
                        dashboard = process_and_summarize_stream(collected_logs, outputs_dir)
                        # Send dashboard summary immediately to the client
                        print(f"Sending dashboard for batch with {len(collected_logs)} logs")
                        yield f"data: {json.dumps(dashboard)}\n\n"
                        collected_logs = []
                        start_time = time.time()
                        await asyncio.sleep(idle_gap)

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# =========================================
# Cleanup
# =========================================
def cleanup_inactive_queues(timeout: int = 3600):
    now = time.time()
    for app_id in list(queue_last_activity.keys()):
        if now - queue_last_activity[app_id] > timeout:
            log_queues.pop(app_id, None)
            queue_last_activity.pop(app_id, None)
