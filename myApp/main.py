from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from services.api_service import ApiService
from services.auth_service import AuthService
from services.inventory_service import InventoryService
from services.notification_service import NotificationService
from services.payment_service import PaymentService

app = FastAPI()

# Allow CORS for frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log_queue = asyncio.Queue()

# Custom log handler to push logs to the queue
class QueueLogHandler(logging.Handler):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    def emit(self, record):
        log_entry = self.format(record)
        try:
            # Use asyncio.create_task to avoid blocking
            asyncio.get_event_loop().call_soon_threadsafe(self.queue.put_nowait, log_entry)
        except Exception:
            pass

# Set up root logger to use our handler
queue_handler = QueueLogHandler(log_queue)
queue_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"))
logging.getLogger().addHandler(queue_handler)
logging.getLogger().setLevel(logging.INFO)

# Service instances (hardcoded ratios, change as needed)
api_service = ApiService(0)
auth_service = AuthService(0)
inventory_service = InventoryService(0)
notification_service = NotificationService(0)
payment_service = PaymentService(0)

# Track the background task globally
service_task = None

# Background task to run all services
async def run_services():
    try:
        await asyncio.gather(
            api_service.run(),
            auth_service.run(),
            inventory_service.run(),
            notification_service.run(),
            payment_service.run()
        )
    except asyncio.CancelledError:
        # Graceful shutdown
        logging.getLogger().info("Service tasks cancelled. Shutting down.")

@app.on_event("startup")
async def startup_event():
    global service_task
    service_task = asyncio.create_task(run_services())

@app.on_event("shutdown")
async def shutdown_event():
    global service_task
    if service_task:
        service_task.cancel()
        try:
            await service_task
        except asyncio.CancelledError:
            pass
        service_task = None

@app.get("/logs/stream")
async def stream_logs():
    async def event_stream():
        while True:
            log_line = await log_queue.get()
            yield f"data: {log_line}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/logs/ratios")
async def set_log_ratios(
    api: int = Body(..., embed=True),
    auth: int = Body(..., embed=True),
    inventory: int = Body(..., embed=True),
    notification: int = Body(..., embed=True),
    payment: int = Body(..., embed=True),
):
    api_service.set_bad_ratio(api)
    auth_service.set_bad_ratio(auth)
    inventory_service.set_bad_ratio(inventory)
    notification_service.set_bad_ratio(notification)
    payment_service.set_bad_ratio(payment)
    return {
        "api": api_service.bad_log_ratio,
        "auth": auth_service.bad_log_ratio,
        "inventory": inventory_service.bad_log_ratio,
        "notification": notification_service.bad_log_ratio,
        "payment": payment_service.bad_log_ratio,
    }
