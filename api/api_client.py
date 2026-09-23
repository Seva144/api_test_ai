import os
import time

from httpx import Client
import logging

from pydantic import json

logger = logging.getLogger(__name__)


def _log_request(request):
    """Вызывается httpx ПЕРЕД отправкой запроса."""
    logger.info(f"→ {request.method} {request.url}")
    if request.content:
        try:
            logger.debug(f"  request body: {request.content.decode('utf-8')}")
        except Exception:
            logger.debug("  request body: <binary>")


def _log_response(response):
    """Вызывается httpx ПОСЛЕ получения ответа."""
    req = response.request
    logger.info(f"← {response.status_code} {req.method} {req.url}")

    if not response.is_stream_consumed:
        try:
            response.read()
        except Exception as e:
            logger.info(f"  response body: <read failed: {type(e).__name__}: {e}>")
            return
    try:
        body = response.json()
        logger.info(f"  response body:\n{json.dumps(body, ensure_ascii=False, indent=2)}")
    except Exception:
        logger.info(f"  response body: {response.text}")


class ApiClient(Client):

    def __init__(self):
        super().__init__(
            base_url=os.getenv("RESOURCE_URL"),
            timeout=30.0,
            event_hooks={
                "request": [_log_request],
                "response": [_log_response],
            },
        )
