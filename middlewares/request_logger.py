from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from utils.request_utils import *
from utils.attack_detection import *
import logging

isMalicious = False

# hiding uvicorn console output
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
        response = await call_next(request)

        request_info = await extract_request_data(request)

        # Log the request details
        logging.info(f"Incoming request: {request_info}")

        result = await sqli_detection(request_info['url'])
        result = await xss_detection(request_info['url'])
        result = await path_traversal_detection(request_info['url'])
        isMalicious = await rce_detection(request_info['url'])

        # if malicious behaviour is detected the request gets redirected
        if isMalicious and request.url.path not in ["/welcome", "/static"]:
            print(f"🔄 Redirecting {request.url.path} to /welcome")
            return RedirectResponse(url="/welcome", status_code=302)

        return response
