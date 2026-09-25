import os


from httpx import Client
import logging

from pydantic import json


class ApiClient(Client):

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger
        super().__init__(
            base_url=os.getenv("RESOURCE_URL"),
            timeout=30.0,
            event_hooks={
                "request": [self._log_request],
                "response": [self._log_response],
            },
        )

    def _log_request(self, request):
        self.logger.info(f"→ {request.method} {request.url}")
        if request.content:
            try:
                self.logger.debug(f"  request body: {request.content.decode('utf-8')}")
            except Exception:
                self.logger.debug("  request body: <binary>")

    def _log_response(self, response):
        req = response.request
        self.logger.info(f"← {response.status_code} {req.method} {req.url}")

        if not response.is_stream_consumed:
            try:
                response.read()
            except Exception as e:
                self.logger.info(f"  response body: <read failed: {type(e).__name__}: {e}>")
                return
        try:
            body = response.json()
            self.logger.info(f"  response body:\n{json.dumps(body, ensure_ascii=False, indent=2)}")
        except Exception:
            self.logger.info(f"  response body: {response.text}")
