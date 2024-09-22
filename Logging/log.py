import logging

# Configure the logger to write to a file
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named 'app.log'
        # logging.StreamHandler()  # Optional: Also log to the console
    ]
)

logger = logging.getLogger(__name__)

# Decorator to log function calls
def log_function_call(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Starting function: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Finished function: {func.__name__}")
        return result
    return wrapper

# Add this at the end of your script to insert a blank line
def log_info(info):
    logger.info(info)