"""
Shared Observability - Logger
Centralized logging configuration for all services
"""
import logging
import sys
from typing import Optional
from datetime import datetime


class ObservabilityLogger:
    """Centralized logger with observability features"""
    
    def __init__(self, service_name: str, level: int = logging.INFO):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)
    
    def log_with_context(self, level: str, message: str, context: dict):
        """Log message with additional context"""
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message, extra={"context": context})


def get_logger(service_name: str) -> ObservabilityLogger:
    """Get logger for a service"""
    return ObservabilityLogger(service_name)


# Example usage
if __name__ == "__main__":
    logger = get_logger("test-service")
    logger.info("Service started")
    logger.log_with_context("info", "Processing request", {"request_id": "123", "user_id": "456"})
