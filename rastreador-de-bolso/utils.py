import logging
import time

logger = logging.getLogger('utils')


def retry(callback, *args, **kwargs):
    # Get retry
    max_retries = kwargs.get('max_retries') if kwargs.get(
        'max_retries') else 10
    retry_delay = kwargs.get('retry_delay') if kwargs.get('retry_delay') else 1
    success = False

    for _ in range(max_retries):
        try:
            global response
            response = callback(*args, **kwargs)
            success = True
            break
        except Exception as e:
            global error
            error = e
            logger.error(e)
            time.sleep(retry_delay)
            continue

    if success:
        return response

    raise error
