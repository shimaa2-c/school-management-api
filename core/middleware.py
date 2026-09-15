import logging
import time
import uuid


logger = logging.getLogger(__name__)


class APIRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Accept an existing request ID or create a new one.
        request_id = request.headers.get("X-Request-ID")

        if not request_id:
            request_id = str(uuid.uuid4())

        # Store it on the request so other parts of the application
        # can access it if needed.
        request.request_id = request_id

        start_time = time.perf_counter()

        response = self.get_response(request)

        duration = (time.perf_counter() - start_time) * 1000

        # Add request ID to every response.
        response["X-Request-ID"] = request_id

        logger.info(
            "method=%s path=%s status=%s request_id=%s duration_ms=%.2f",
            request.method,
            request.path,
            response.status_code,
            request_id,
            duration,
        )

        return response