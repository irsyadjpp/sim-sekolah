"""
Shared logging configuration for AI Platform services

This module provides centralized logging configuration that can be used
across all services to ensure consistent log formatting and handling.
"""

import logging
import sys
from typing import Optional
from pathlib import Path
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'service_name'):
            log_data["service"] = record.service_name
        if hasattr(record, 'request_id'):
            log_data["request_id"] = record.request_id
        if hasattr(record, 'user_id'):
            log_data["user_id"] = record.user_id
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for development."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        # Custom format
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return formatter.format(record)


def setup_logging(
    service_name: str,
    level: str = "INFO",
    log_format: str = "text",  # "text" or "json"
    log_file: Optional[str] = None,
    enable_console: bool = True,
) -> logging.Logger:
    """
    Setup logging for a service.
    
    Args:
        service_name: Name of the service
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format ("text" or "json")
        log_file: Optional file path for log output
        enable_console: Whether to enable console logging
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()  # Clear existing handlers
    
    # Service name as extra field
    old_factory = logging.getLogRecordFactory()
    
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.service_name = service_name
        return record
    
    logging.setLogRecordFactory(record_factory)
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        if log_format == "json":
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(ColoredFormatter())
        
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class RequestContext:
    """Context manager for adding request-specific context to logs."""
    
    def __init__(self, logger: logging.Logger, request_id: str, user_id: Optional[str] = None):
        """
        Initialize request context.
        
        Args:
            logger: Logger instance
            request_id: Request ID
            user_id: Optional user ID
        """
        self.logger = logger
        self.request_id = request_id
        self.user_id = user_id
        self.old_factory = logging.getLogRecordFactory()
    
    def __enter__(self):
        """Add request context to log records."""
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            record.request_id = self.request_id
            if self.user_id:
                record.user_id = self.user_id
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Remove request context from log records."""
        logging.setLogRecordFactory(self.old_factory)


def log_function_call(logger: logging.Logger):
    """
    Decorator to log function calls.
    
    Args:
        logger: Logger instance
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed with error: {e}", exc_info=True)
                raise
        return wrapper
    return decorator


# Default logger setup
default_logger = setup_logging("ai-platform", level="INFO", log_format="text")