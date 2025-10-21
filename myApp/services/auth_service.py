import asyncio
import random
try:
    # When imported as a module
    from functions.logger import get_logger
except ImportError:
    # When imported directly
    from ..functions.logger import get_logger

logger = get_logger("AuthService")

class AuthService:
    def __init__(self, bad_log_ratio: int = 2):
        self.bad_log_ratio = bad_log_ratio
        logger.info(f"Auth Service initialized with bad_log_ratio: {bad_log_ratio}")
    
    def set_bad_ratio(self, ratio: int):
        """Update the bad log ratio for this service"""
        if not isinstance(ratio, int) or not (0 <= ratio <= 10):
            logger.error(f"Invalid bad_log_ratio: {ratio}, must be between 0-10")
            return
        logger.info(f"Updating Auth Service bad_log_ratio: {self.bad_log_ratio} -> {ratio}")
        self.bad_log_ratio = ratio
    
    async def run(self):
        """
        Simulate authentication service.
        bad_log_ratio: number of bad logs per 10 logs (0-10)
        """
        log_count = 0
        while True:
            log_count += 1
            user_id = random.randint(1000, 9999)
            username = f"user_{random.randint(100, 999)}"
            client_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            
            if self.bad_log_ratio == 0:
                # Always good logs
                actions = ["login", "logout", "password_change", "token_refresh", "two_factor_auth", "profile_update"]
                action = random.choice(actions)
                
                logger.info(f"User {username} (ID: {user_id}) requested {action} from {client_ip}")
                
                if action == "login":
                    logger.info(f"Successful login for user {username} (ID: {user_id})")
                    logger.debug(f"Auth token issued for user {user_id}, valid for 24 hours")
                    if random.random() < 0.2:
                        logger.info(f"First login from new device for user {username}")
                elif action == "logout":
                    logger.info(f"User {username} logged out successfully")
                elif action == "token_refresh":
                    logger.info(f"Token refreshed for user {username}")
                    logger.debug(f"New token issued with extended expiry")
                elif action == "two_factor_auth":
                    logger.info(f"2FA verification successful for user {username}")
                elif action == "password_change":
                    logger.info(f"Password updated for user {username}")
                    logger.debug(f"Password policy check passed for user {user_id}")
            
            elif log_count % 10 < self.bad_log_ratio:
                # Bad logs
                error_types = ["auth_failure", "token_expired", "suspicious_activity", "rate_limit", "server_error"]
                error_type = random.choice(error_types)
                
                if error_type == "auth_failure":
                    logger.warning(f"Failed login attempt for user {username} from {client_ip}")
                    logger.warning(f"Multiple failed login attempts for user {username}")
                    if random.random() < 0.5:
                        logger.error(f"Account temporarily locked for user {username} due to failed attempts")
                
                elif error_type == "token_expired":
                    logger.warning(f"Expired token used by user {username}")
                    logger.debug(f"Token expired 30 minutes ago for user {user_id}")
                
                elif error_type == "suspicious_activity":
                    logger.warning(f"Suspicious activity for user {username} (IP mismatch)")
                    logger.warning(f"Location change detected for user {username}: New York -> London")
                    if random.random() < 0.5:
                        logger.error(f"Potential account breach attempt for user {username}")
                
                elif error_type == "rate_limit":
                    logger.warning(f"Rate limit exceeded for user {username}")
                    logger.info(f"Too many requests from {client_ip}")
                
                elif error_type == "server_error":
                    logger.error(f"Auth server timeout while validating user {username}")
                    logger.error(f"LDAP connection failure during authentication for user {username}")
                    logger.debug(f"Connection timeout after 30s to LDAP server")
            
            else:
                # Good logs
                actions = ["login", "logout", "password_change", "token_refresh", "two_factor_auth", "profile_update"]
                action = random.choice(actions)
                
                logger.info(f"User {username} (ID: {user_id}) requested {action} from {client_ip}")
                
                if action == "login":
                    logger.info(f"Successful login for user {username} (ID: {user_id})")
                    logger.debug(f"Auth token issued for user {user_id}, valid for 24 hours")
                    if random.random() < 0.2:
                        logger.info(f"First login from new device for user {username}")
                elif action == "logout":
                    logger.info(f"User {username} logged out successfully")
                elif action == "token_refresh":
                    logger.info(f"Token refreshed for user {username}")
                    logger.debug(f"New token issued with extended expiry")
                elif action == "two_factor_auth":
                    logger.info(f"2FA verification successful for user {username}")
                elif action == "password_change":
                    logger.info(f"Password updated for user {username}")
                    logger.debug(f"Password policy check passed for user {user_id}")
            
            await asyncio.sleep(random.uniform(2, 5))
