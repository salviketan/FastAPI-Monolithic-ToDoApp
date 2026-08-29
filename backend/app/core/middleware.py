import time
from typing import Any

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import api_logger, debug_logger


class APILoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time: float = time.time()
        method: str = request.method
        path: str = request.url.path
        client_ip: str = request.client.host if request.client else "unknown"

        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
        response: Response | None = None

        try:
            response: Any = await call_next(request)
            status_code: int = response.status_code
            return response
        except Exception as exc:
            # 1. Log full stack trace ONLY in debug.log
            debug_logger.exception(
                "Unhandled Server Error on '%s %s' from IP: %s", method, path, client_ip
            )

            raise exc
        finally:
            # 2. Always compute process time and log single-line metric to api.log
            process_time: float = (time.time() - start_time) * 1000
            # 3. Format the log string
            log_message: str = (
                f"IP: {client_ip} - '{method} {path}' "
                f"Status: {status_code} Completed in: {process_time:.2f}ms"
            )

            if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
                api_logger.error(log_message)
            elif status_code >= status.HTTP_400_BAD_REQUEST:
                api_logger.warning(log_message)
            else:
                api_logger.info(log_message)
