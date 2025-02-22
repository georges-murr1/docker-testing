from loguru import logger

# Configure loguru logging
logger.add("logs/app.log", rotation="10MB", retention="10 days", level="INFO")

def log_error(message: str):
    logger.error(message)

def log_info(message: str):
    logger.info(message)
