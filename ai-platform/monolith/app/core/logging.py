"""
Logging Configuration for Monolith Architecture
"""
import logging
import sys
from typing import Optional

def setup_logging(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Setup logging configuration for the monolith
    
    Args:
        service_name: Name of the service for logging context
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Prevent duplicate handlers
    logger.propagate = False
    
    return logger