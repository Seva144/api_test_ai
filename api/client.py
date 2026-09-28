import os


from httpx import Client
import logging

from pydantic import json

from utilities.log_utils import pretty_json


class ApiClient(Client):

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger
        super().__init__(
            base_url=os.getenv("RESOURCE_URL"),
            timeout=120.0,
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
                self.logger.debug("  request body:\n%s", pretty_json(request.content))

    def _log_response(self, response):
        req = response.request
        self.logger.info(f"← {response.status_code} {req.method} {req.url}")

        content_type = response.headers.get("content-type", "")
        if "text/event-stream" in content_type:
            self.logger.debug("  response body: <SSE stream, skipped>")
            return
        if not response.is_stream_consumed:
            try:
                response.read()
            except Exception as e:
                self.logger.info(f"  response body: <read failed: {type(e).__name__}: {e}>")
                return
        self.logger.info("  response body:\n%s", pretty_json(response.content))

