import asyncio
import random
try:
    # When imported as a module
    from functions.logger import get_logger
except ImportError:
    # When imported directly
    from ..functions.logger import get_logger

logger = get_logger("NotificationService")

class NotificationService:
    def __init__(self, bad_log_ratio: int = 2):
        self.bad_log_ratio = bad_log_ratio
        logger.info(f"Notification Service initialized with bad_log_ratio: {bad_log_ratio}")
    
    def set_bad_ratio(self, ratio: int):
        """Update the bad log ratio for this service"""
        if not isinstance(ratio, int) or not (0 <= ratio <= 10):
            logger.error(f"Invalid bad_log_ratio: {ratio}, must be between 0-10")
            return
        logger.info(f"Updating Notification Service bad_log_ratio: {self.bad_log_ratio} -> {ratio}")
        self.bad_log_ratio = ratio
    
    async def run(self):
        """
        Simulate notification service.
        bad_log_ratio: number of bad logs per 10 logs (0-10)
        """
        log_count = 0
        notification_types = ["email", "sms", "push", "in_app", "webhook"]
        notification_events = ["order_confirmation", "shipping_update", "password_reset", "account_alert", 
                             "payment_confirmation", "promotional", "security_alert", "system_update"]
        
        while True:
            log_count += 1
            user_id = random.randint(1000, 9999)
            notification_id = f"NOTIF-{random.randint(10000, 99999)}"
            notification_type = random.choice(notification_types)
            event = random.choice(notification_events)
            
            # Good logs
            if log_count % 10 > self.bad_log_ratio:
                # Prepare notification
                logger.info(f"Preparing {notification_type} notification {notification_id} for user {user_id}")
                logger.debug(f"Notification template loaded: {event.replace('_', '-')}.template")
                
                # Send notification
                logger.info(f"Sending {notification_type} notification for event: {event.replace('_', ' ')}")
                
                if notification_type == "email":
                    delivery_time = random.randint(100, 600)
                    logger.info(f"Email notification {notification_id} sent to user {user_id}")
                    logger.debug(f"Email delivery time: {delivery_time}ms")
                    
                    if random.random() < 0.2:
                        logger.info(f"Email opened by user {user_id}")
                
                elif notification_type == "sms":
                    logger.info(f"SMS notification {notification_id} sent to user {user_id}")
                    logger.debug(f"SMS provider: {'Twilio' if random.random() < 0.7 else 'Nexmo'}")
                
                elif notification_type == "push":
                    platforms = ["iOS", "Android", "Web"]
                    platform = random.choice(platforms)
                    logger.info(f"Push notification {notification_id} sent to user {user_id} on {platform}")
                    
                    if random.random() < 0.3:
                        logger.info(f"Push notification clicked by user {user_id}")
                
                elif notification_type == "in_app":
                    logger.info(f"In-app notification {notification_id} delivered to user {user_id}")
                    
                    if random.random() < 0.4:
                        logger.info(f"In-app notification viewed by user {user_id}")
                
                elif notification_type == "webhook":
                    target = f"https://api.external-{random.randint(1, 99)}.com/webhook"
                    logger.info(f"Webhook notification {notification_id} sent to {target}")
                    logger.debug(f"Webhook payload size: {random.randint(0, 10)}KB")
            
            # Bad logs
            else:
                error_types = ["delivery_failed", "rate_limit", "template_error", "user_not_found", "service_down"]
                error_type = random.choice(error_types)
                
                if error_type == "delivery_failed":
                    logger.error(f"{notification_type.title()} notification {notification_id} delivery failed")
                    
                    if notification_type == "email":
                        bounce_reasons = ["mailbox full", "invalid address", "spam rejected", "server unavailable"]
                        reason = random.choice(bounce_reasons)
                        logger.warning(f"Email bounce for user {user_id}: {reason}")
                        logger.info(f"Scheduling email retry in {random.randint(15, 120)} minutes")
                    
                    elif notification_type == "sms":
                        logger.warning(f"SMS delivery failed to user {user_id}: invalid number")
                    
                    elif notification_type == "push":
                        logger.warning(f"Push notification failed: device token expired for user {user_id}")
                        logger.info(f"Removing invalid device token for user {user_id}")
                
                elif error_type == "rate_limit":
                    logger.warning(f"Rate limit reached for {notification_type} notifications")
                    logger.info(f"Queueing notification {notification_id} for delayed delivery")
                    logger.debug(f"Current queue size: {random.randint(10, 100)} notifications")
                
                elif error_type == "template_error":
                    logger.error(f"Template rendering failed for notification {notification_id}")
                    logger.debug(f"Missing variable in template: {{user_firstname}}")
                    logger.warning(f"Using fallback template for event {event}")
                
                elif error_type == "user_not_found":
                    logger.error(f"Failed to send notification {notification_id}: user {user_id} not found")
                    logger.warning(f"Notification marked as undeliverable for event {event}")
                
                elif error_type == "service_down":
                    if notification_type in ["email", "sms"]:
                        provider = "SendGrid" if notification_type == "email" else "Twilio"
                        logger.error(f"{provider} service unavailable for {notification_type} delivery")
                        logger.warning(f"Switching to backup provider for {notification_type} notifications")
                    else:
                        logger.error(f"Notification subsystem unavailable for {notification_type} messages")
                        logger.warning(f"Circuit breaker triggered for notification service")
                        logger.debug(f"Attempting service restart in {random.randint(30, 300)} seconds")
            
            await asyncio.sleep(random.uniform(1.0, 3.0))
