from NestView.logger import logger
from NestView.custom_exception import InvalidURLException

try:
    raise InvalidURLException()
except Exception as e:
    logger.error(f"An error occurred: {e}")