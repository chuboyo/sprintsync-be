import time
import logging
import traceback
from django.utils.timezone import now
from django.utils.functional import SimpleLazyObject

logger = logging.getLogger(__name__)

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()

        # Capture the user id lazily (avoids hitting DB before authentication)
        def get_user_id():
            return getattr(request.user, 'id', None) if hasattr(request, 'user') else None
        request.user_id = SimpleLazyObject(get_user_id)

        try:
            response = self.get_response(request)
        except Exception as e:
            latency = int((time.perf_counter() - start_time) * 1000)
            self.log_error(request, e, latency)
            raise

        latency = int((time.perf_counter() - start_time) * 1000)
        self.log_request(request, response, latency)
        return response

    def log_request(self, request, response, latency):
        log_data = {
            "timestamp": now().isoformat(),
            "method": request.method,
            "path": request.get_full_path(),
            "user_id": getattr(request, "user_id", None),
            "status_code": response.status_code,
            "latency_ms": latency,
        }
        logger.info("API Request", extra=log_data)

    def log_error(self, request, exception, latency):
        log_data = {
            "timestamp": now().isoformat(),
            "method": request.method,
            "path": request.get_full_path(),
            "user_id": getattr(request, "user_id", None),
            "latency_ms": latency,
            "error": str(exception),
            "stack_trace": traceback.format_exc()
        }
        logger.error("API Error", extra=log_data)
