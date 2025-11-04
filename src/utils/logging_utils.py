"""
Logging utilities for structured logging across the application.
"""
import logging
import logging.config
import os
import yaml
from pathlib import Path
from typing import Optional


def setup_logging(
    config_path: Optional[str] = None,
    log_level: Optional[str] = None,
    log_dir: Optional[str] = "logs"
) -> None:
    """
    Setup logging configuration from YAML file or defaults.

    Args:
        config_path: Path to logging configuration YAML file
        log_level: Override log level from environment
        log_dir: Directory for log files

    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    if config_path and Path(config_path).exists():
        # Load configuration from YAML
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    else:
        # Use basic configuration if YAML not found
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        level = getattr(logging, log_level or os.getenv("LOG_LEVEL", "INFO"))

        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(f"{log_dir}/app.log")
            ]
        )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Name of the module (typically __name__)

    Returns:
        Logger instance configured for the module
    """
    return logging.getLogger(name)


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.

    Usage:
        class MyClass(LoggerMixin):
            def my_method(self):
                self.logger.info("Log message")
    """

    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__module__)


def log_function_call(func):
    """
    Decorator to log function calls with parameters and return values.

    Usage:
        @log_function_call
        def my_function(arg1, arg2):
            return result
    """
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")

        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned {type(result).__name__}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {str(e)}")
            raise

    return wrapper


def log_execution_time(func):
    """
    Decorator to log function execution time.

    Usage:
        @log_execution_time
        def slow_function():
            # ... do work ...
    """
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f}s: {str(e)}")
            raise

    return wrapper
