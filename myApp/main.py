from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import logging
from services.api_service import ApiService
from services.auth_service import AuthService
from services.inventory_service import InventoryService
from services.notification_service import NotificationService
from services.payment_service import PaymentService

app = FastAPI()
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
api_service = ApiService(2)
auth_service = AuthService(2)
inventory_service = InventoryService(2)
notification_service = NotificationService(2)
payment_service = PaymentService(2)

# Background task to run all services
async def run_services():
    await asyncio.gather(
        api_service.run(),
        auth_service.run(),
        inventory_service.run(),
        notification_service.run(),
        payment_service.run()
    )

@app.on_event("startup")
async def startup_event():
    # Start the services in the background
    asyncio.create_task(run_services())

@app.get("/logs/stream")
async def stream_logs():
    async def event_stream():
        while True:
            log_line = await log_queue.get()
            yield f"data: {log_line}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
