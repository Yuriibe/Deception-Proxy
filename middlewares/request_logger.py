from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from utils.request_utils import extract_request_data
import logging

uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access", "watchfiles"]
for logger_name in uvicorn_loggers:
    logging.getLogger(logger_name).propagate = False

# Configure logging only for our middleware logs
logging.basicConfig(
    filename="logs/request_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        print("🔍 Middleware is running for request:", request.url)  # Debugging print
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        request_info = await extract_request_data(request)

        # Log the request details
        print("Extracted Request Data:", request_info)  # Debugging print
        logging.info(f"Incoming request: {request_info}")  # Ensure this logs only request_data

        return response