import asyncio
import random
try:
    # When imported as a module
    from functions.logger import get_logger
except ImportError:
    # When imported directly
    from ..functions.logger import get_logger

logger = get_logger("PaymentService")

class PaymentService:
    def __init__(self, bad_log_ratio: int = 2):
        self.bad_log_ratio = bad_log_ratio
        logger.info(f"Payment Service initialized with bad_log_ratio: {bad_log_ratio}")
    
    def set_bad_ratio(self, ratio: int):
        """Update the bad log ratio for this service"""
        if not isinstance(ratio, int) or not (0 <= ratio <= 10):
            logger.error(f"Invalid bad_log_ratio: {ratio}, must be between 0-10")
            return
        logger.info(f"Updating Payment Service bad_log_ratio: {self.bad_log_ratio} -> {ratio}")
        self.bad_log_ratio = ratio
    
    async def run(self):
        """
        Simulate payment service.
        bad_log_ratio: number of bad logs per 10 logs (0-10)
        """
        log_count = 0
        payment_methods = ["credit_card", "debit_card", "paypal", "bank_transfer", "crypto", "apple_pay", "google_pay"]
        card_types = ["Visa", "Mastercard", "Amex", "Discover"]
        currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
        
        while True:
            log_count += 1
            txn_id = f"TXN-{random.randint(100000, 999999)}"
            order_id = f"ORD-{random.randint(10000, 99999)}"
            user_id = random.randint(1000, 9999)
            payment_method = random.choice(payment_methods)
            amount = round(random.uniform(10, 2000), 2)
            currency = random.choice(currencies)
            
            # Good logs
            if log_count % 10 > self.bad_log_ratio:
                logger.info(f"Payment initiated: {txn_id} for order {order_id} - {currency} {amount}")
                
                if payment_method in ["credit_card", "debit_card"]:
                    card_type = random.choice(card_types)
                    last_four = f"{random.randint(1000, 9999)}"
                    logger.info(f"Processing {card_type} payment ending in {last_four} for {txn_id}")
                    logger.debug(f"Card verification successful for transaction {txn_id}")
                
                elif payment_method in ["paypal", "apple_pay", "google_pay"]:
                    logger.info(f"Processing {payment_method.replace('_', ' ').title()} payment for {txn_id}")
                    logger.debug(f"External payment provider authentication successful")
                
                elif payment_method == "bank_transfer":
                    logger.info(f"Bank transfer initiated for {txn_id}")
                    logger.debug(f"ACH transfer details: {random.randint(100000, 999999)}")
                
                logger.info(f"Payment {txn_id} successfully processed for user {user_id}")
                logger.debug(f"Transaction time: {random.randint(200, 1500)}ms")
                
                # Sometimes add receipt info
                if random.random() < 0.3:
                    logger.info(f"Receipt generated for transaction {txn_id}")
                    logger.debug(f"Receipt delivery: Email to user {user_id}")
            
            # Bad logs
            else:
                error_types = ["payment_declined", "processing_error", "timeout", "fraud_check", "system_error"]
                error_type = random.choice(error_types)
                
                if error_type == "payment_declined":
                    decline_reasons = ["insufficient_funds", "card_expired", "invalid_details", "limit_exceeded"]
                    reason = random.choice(decline_reasons)
                    logger.warning(f"Payment {txn_id} declined: {reason.replace('_', ' ')}")
                    logger.error(f"Order {order_id} payment failed: {reason.replace('_', ' ')}")
                    logger.debug(f"Payment gateway response code: {random.randint(100, 999)}")
                
                elif error_type == "processing_error":
                    logger.error(f"Payment processing error for transaction {txn_id}")
                    logger.warning(f"Payment gateway connection unstable during transaction {txn_id}")
                    logger.debug(f"Retry attempt {random.randint(1, 3)} of 3")
                
                elif error_type == "timeout":
                    logger.error(f"Payment gateway timeout for transaction {txn_id}")
                    logger.warning(f"Payment confirmation delayed for order {order_id}")
                    logger.debug(f"Timeout after {random.randint(30, 60)} seconds")
                
                elif error_type == "fraud_check":
                    logger.warning(f"Fraud check triggered for transaction {txn_id}")
                    logger.info(f"Manual review required for transaction {txn_id}")
                    if random.random() < 0.5:
                        logger.error(f"Transaction {txn_id} rejected by fraud detection system")
                        logger.debug(f"Fraud score: {random.randint(800, 950)}/1000")
                
                elif error_type == "system_error":
                    logger.error(f"Payment system error during transaction {txn_id}")
                    logger.error(f"Database connection failed during payment processing")
                    logger.debug(f"Stack trace: ConnectionError in ProcessPayment() method")
            
            await asyncio.sleep(random.uniform(1.0, 3.5))
