import logging
from config import Config

logger = logging.getLogger(__name__)

def configure_logger(level=Config.LOGGING_LEVEL):
    """
    Configures the logger based on the provided log level.

    Args:
        level (str): The logging level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL). 
            Defaults to Config.LOGGING_LEVEL.
    """
    logger.setLevel(level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the formatter to the handler
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Optional: Create a file handler for storing logs in a file
    # file_handler = logging.FileHandler("app.log")
    # file_handler.setLevel(level)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

# Configure the logger at the module level
configure_logger()

def debug(message, *args, **kwargs):
    """Logs a debug message."""
    logger.debug(message, *args, **kwargs)

def info(message, *args, **kwargs):
    """Logs an info message."""
    logger.info(message, *args, **kwargs)

def warning(message, *args, **kwargs):
    """Logs a warning message."""
    logger.warning(message, *args, **kwargs)

def error(message, *args, **kwargs):
    """Logs an error message."""
    logger.error(message, *args, **kwargs)

def critical(message, *args, **kwargs):
    """Logs a critical message."""
    logger.critical(message, *args, **kwargs)