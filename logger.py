import logging
import functools

# Create a logger instance
# logger = logging.getLogger(func.__name__)
logging.basicConfig(filename="log_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the function call and its arguments
        logger.info(f"Function {func.__name__} called with args: {args}, kwargs: {kwargs}")

        # Call the original function and get its return value
        result = func(*args, **kwargs)

        # Log the function's return value
        logger.info(f"Function {func.__name__} returned: {result}")

        return result

    return wrapper
