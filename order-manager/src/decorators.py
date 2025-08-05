import time
from functools import wraps

def retry_decorator(max_retries, delay):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            logger = getattr(self, 'logger', None)
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if logger:
                        logger.warning(f"Attempt {attempt + 1} failed: {err}")
                    if attempt == max_retries:
                        if logger:
                            logger.error("Max retries reached. Raising exception.")
                        raise err
                    time.sleep(delay)
        return wrapper
    return decorator