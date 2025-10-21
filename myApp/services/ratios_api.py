from fastapi import APIRouter, Body
from . import api_service, auth_service, inventory_service, notification_service, payment_service

router = APIRouter()

@router.post("/logs/ratios")
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
