from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
import os
from services.api_service import ApiService
from services.auth_service import AuthService
from services.inventory_service import InventoryService
from services.notification_service import NotificationService
from services.payment_service import PaymentService

app = FastAPI()

# Allow CORS for frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Sentry Logger SDK (optional)
# If SDK is installed and API key is set, logs will be sent to Sentry backend
try:
    import sentry_logger as sentry
    api_key = os.environ.get("LOGSENTRY_API_KEY", "")
    
    if api_key:
        sentry.init(api_key=api_key)
        logging.info("✅ LogSentry SDK initialized - logs will be sent to dashboard")
    else:
        logging.info("ℹ️  LOGSENTRY_API_KEY not set - logs will only go to console")
except ImportError:
    logging.info("ℹ️  LogSentry SDK not installed - logs will only go to console")
    logging.info("    To send logs to dashboard: pip install logsentry-sdk")
except Exception as e:
    logging.warning(f"⚠️  Failed to initialize LogSentry SDK: {e}")

# Service instances (bad log ratio 0-10 per service)
api_service = ApiService(0)
auth_service = AuthService(0)
inventory_service = InventoryService(0)
notification_service = NotificationService(0)
payment_service = PaymentService(0)

# Track the background task globally
service_task = None


async def run_services():
    try:
        await asyncio.gather(
            api_service.run(),
            auth_service.run(),
            inventory_service.run(),
            notification_service.run(),
            payment_service.run(),
        )
    except asyncio.CancelledError:
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


@app.post("/logs/ratios")
async def set_log_ratios(
    api: int = Body(..., embed=True),
    auth: int = Body(..., embed=True),
    inventory: int = Body(..., embed=True),
    notification: int = Body(..., embed=True),
    payment: int = Body(..., embed=True),
):
    """Adjust error log ratios for demo (0-10 per service)."""
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
