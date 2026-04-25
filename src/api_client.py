import os
import logging

from dotenv import load_dotenv
from httpx import Client, Response, Timeout

logger = logging.getLogger(__name__)

# клиент для отправки запросов
class ApiClient(Client):
    def __init__(self, base_url: str = None, timeout: int = 10):

        load_dotenv()

        self.base_url_str = base_url or os.getenv("RESOURSE_URL")

        if not self.base_url_str:
            raise ValueError("RESOURCE_URL environment variable is not set")

        full_base_url = f"https://{self.base_url_str}"
        timeout_config = Timeout(timeout=timeout)

        super().__init__(
            base_url=full_base_url,
            timeout=timeout_config,
            headers={"Content-Type": "application/json"}
        )

        self.use_logs = os.getenv("USE_LOGS", "false").lower() in ("true", "1", "yes")

    def request(self, method: str, url: str, **kwargs) -> Response:
        if self.use_logs:
            logger.info(f"➡️ {method} {url}")

        response = super().request(method, url, **kwargs)

        if self.use_logs:
            logger.info(f"⬅️ Status: {response.status_code} | Body: {response.text[:200]}")

        return response