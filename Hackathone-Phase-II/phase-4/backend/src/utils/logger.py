import logging
from datetime import datetime
from typing import Optional
import json

# Configure the root logger
logging.basicConfig(level=logging.INFO)

# Create a custom logger for the application
logger = logging.getLogger(__name__)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)

class SecurityLogger:
    """Custom logger for security-related events."""

    @staticmethod
    def log_task_access_attempt(user_id: int, task_id: int, action: str, success: bool, ip_address: Optional[str] = None):
        """Log task access attempts for security monitoring."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "task_access",
            "user_id": user_id,
            "task_id": task_id,
            "action": action,
            "success": success,
            "ip_address": ip_address
        }

        log_message = f"Task access attempt: {json.dumps(log_data)}"

        if success:
            logger.info(log_message)
        else:
            logger.warning(log_message)

    @staticmethod
    def log_authentication_event(event_type: str, user_id: Optional[int] = None, ip_address: Optional[str] = None, details: Optional[str] = None):
        """Log authentication events for security monitoring."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "ip_address": ip_address,
            "details": details
        }

        log_message = f"Authentication event: {json.dumps(log_data)}"

        if event_type in ["login_success", "logout"]:
            logger.info(log_message)
        elif event_type in ["login_failure", "auth_failure", "access_denied"]:
            logger.warning(log_message)
        else:
            logger.info(log_message)

    @staticmethod
    def log_unauthorized_access(endpoint: str, user_id: Optional[int] = None, ip_address: Optional[str] = None):
        """Log unauthorized access attempts."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "unauthorized_access",
            "endpoint": endpoint,
            "user_id": user_id,
            "ip_address": ip_address
        }

        log_message = f"Unauthorized access attempt: {json.dumps(log_data)}"
        logger.warning(log_message)

# Convenience functions
def log_task_access(user_id: int, task_id: int, action: str, success: bool = True, ip_address: Optional[str] = None):
    """Convenience function to log task access."""
    SecurityLogger.log_task_access_attempt(user_id, task_id, action, success, ip_address)

def log_auth_event(event_type: str, user_id: Optional[int] = None, ip_address: Optional[str] = None, details: Optional[str] = None):
    """Convenience function to log authentication events."""
    SecurityLogger.log_authentication_event(event_type, user_id, ip_address, details)

def log_unauthorized(endpoint: str, user_id: Optional[int] = None, ip_address: Optional[str] = None):
    """Convenience function to log unauthorized access."""
    SecurityLogger.log_unauthorized_access(endpoint, user_id, ip_address)