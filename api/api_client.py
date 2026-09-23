import os

from httpx import Client
import logging

logger = logging.getLogger(__name__)


class ApiClient(Client):

    def __init__(self):
        super().__init__(
            base_url=f"{os.getenv('RESOURCE_URL')}",
            timeout=30.0
        )

    def request(self, method, url, **kwargs):
        # собрать запрос, чтобы знать финальный URL, тело и заголовки
        request = super().request(method, url, **kwargs)
        full_url = str(request.url)

        # --- лог запроса ---
        logger.info(f"→ {method} {full_url}")
        if request.content:
            logger.debug(f"  request body: {request.content.decode('utf-8')}")

        # --- отправить ---
        start = time.perf_counter()
        try:
            response = self.send(request)
        except Exception as e:
            logger.exception(f"✘ {method} {full_url} — {type(e).__name__}: {e}")
            raise
        elapsed_ms = (time.perf_counter() - start) * 1000

        # --- лог ответа ---
        logger.info(f"← {response.status_code} {method} {full_url} ({elapsed_ms:.0f} ms)")
        try:
            logger.debug(f"  response body: {response.text}")
        except Exception:
            logger.debug("  response body: <binary or unreadable>")

        return response
