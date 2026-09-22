import os

from httpx import Client, Response
from utilities.logger_utils import logger


class ApiClient:

    def __init__(self):
        super().__init__(base_url=f"https://{os.getenv('RESOURCE_URL')}")

    def request(self, method, url, **kwargs):
        if eval(os.getenv("USE_LOGS")):
            logger.info(f'{method} {url}')
        return super().request(method, url, **kwargs)
