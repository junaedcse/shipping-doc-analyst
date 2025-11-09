"""Logging configuration for the application."""
import logging
import sys
from pathlib import Path
from loguru import logger

def setup_logger(log_level: str = "INFO", log_file: str | None = None) -> None:
    """Configure logger with console and file handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file (optional)
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with colors
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
    )
    
    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            rotation="10 MB",
            retention="1 week",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
        )
    
    logger.info(f"Logger configured with level: {log_level}")

# Create a module-level logger instance
log = logger
