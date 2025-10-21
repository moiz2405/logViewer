import random
import asyncio
try:
    # When imported as a module
    from functions.logger import get_logger
except ImportError:
    # When imported directly
    from ..functions.logger import get_logger

logger = get_logger("ApiService")

class ApiService:
    def __init__(self, bad_log_ratio: int = 2):
        self.bad_log_ratio = bad_log_ratio
        logger.info(f"API Service initialized with bad_log_ratio: {bad_log_ratio}")
    
    def set_bad_ratio(self, ratio: int):
        """Update the bad log ratio for this service"""
        if not isinstance(ratio, int) or not (0 <= ratio <= 10):
            logger.error(f"Invalid bad_log_ratio: {ratio}, must be between 0-10")
            return
        logger.info(f"Updating API Service bad_log_ratio: {self.bad_log_ratio} -> {ratio}")
        self.bad_log_ratio = ratio
    
    async def run(self):
        """
        Simulate API service.
        bad_log_ratio: number of bad logs per 10 logs (0-10)
        """
        log_count = 0
        endpoints = ["users", "products", "orders", "categories", "search"]
        http_methods = ["GET", "POST", "PUT", "DELETE"]
        
        while True:
            log_count += 1
            req_id = random.randint(10000, 99999)
            endpoint = random.choice(endpoints)
            method = random.choice(http_methods)
            client_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            response_time = random.randint(10, 400)

            # Good logs
            if self.bad_log_ratio == 0:
                # Always good logs
                logger.info(f"API {method} /{endpoint} - Request {req_id} handled successfully from {client_ip}")
                logger.debug(f"API response time: {response_time}ms for request {req_id}")
                if random.random() < 0.3:
                    logger.info(f"Cache hit for API request {req_id} on /{endpoint}")
                if response_time > 300:
                    logger.warning(f"Slow response detected: {response_time}ms for request {req_id}")
            elif log_count % 10 < self.bad_log_ratio:
                # Bad logs
                status_codes = [400, 401, 403, 404, 500, 502, 503]
                error_code = random.choice(status_codes)
                if error_code < 500:
                    logger.warning(f"API {method} /{endpoint} - Request {req_id} failed with {error_code}")
                    if error_code == 401:
                        logger.warning(f"Authentication failed for request {req_id} from {client_ip}")
                    elif error_code == 403:
                        logger.warning(f"Permission denied for request {req_id} accessing /{endpoint}")
                    elif error_code == 404:
                        logger.warning(f"Resource not found: /{endpoint} for request {req_id}")
                else:
                    logger.error(f"API {method} /{endpoint} - Request {req_id} failed with {error_code} Internal Server Error")
                    if error_code == 500:
                        logger.error(f"Unhandled exception in API handler for request {req_id}")
                        logger.debug(f"Stack trace for request {req_id}: KeyError: 'user_id' in process_request()")
                    elif error_code == 502:
                        logger.error(f"Bad Gateway error connecting to upstream service for request {req_id}")
                    elif error_code == 503:
                        logger.error(f"Service Unavailable - Database connection timeout for request {req_id}")
                        logger.warning(f"Database connection pool exhausted during request {req_id}")
            else:
                # Good logs
                logger.info(f"API {method} /{endpoint} - Request {req_id} handled successfully from {client_ip}")
                logger.debug(f"API response time: {response_time}ms for request {req_id}")
                if random.random() < 0.3:
                    logger.info(f"Cache hit for API request {req_id} on /{endpoint}")
                if response_time > 300:
                    logger.warning(f"Slow response detected: {response_time}ms for request {req_id}")
            await asyncio.sleep(random.uniform(2, 5))
