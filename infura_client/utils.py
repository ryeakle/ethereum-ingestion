import random
import time


def retry_with_exponential_backoff(func):
    """
    decorator for executing a function with automatic retries with exponential backoff and jitter
    e.g.
    @retry_with_exponential_backoff
    def create_connection_with_service(...):
        ...
    """

    def retry(*args, **kwargs):
        max_retries = 3
        for retry_count in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                caught_exception = e
                print(
                    f"caught exception: {caught_exception}; (retry count: {retry_count})"
                )
                if retry_count + 1 < max_retries:
                    time.sleep(2 ** (retry_count + 1) + random.random() * 3)
        else:
            raise caught_exception

    return retry
