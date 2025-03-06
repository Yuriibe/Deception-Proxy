from dto.request_dto import RequestDTO
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse, Response
from utils.request_utils import *
from utils.attack_detection import *
import logging
from services.request_service import RequestService
from services.FakeDataService import FakeDataService

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
fakeService = FakeDataService()


class RequestLoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        request_info = await extract_request_data(request)
        # Log the request details
        logging.info(f"Incoming request: {request_info}")
        is_SQLi = await sqli_detection(request_info['url'])
        is_XSS = await xss_detection(request_info['url'])
        is_PathTraversal = await path_traversal_detection(request_info['url'])
        is_RCE = await rce_detection(request_info['url'])

        attack_type = None

        match (is_SQLi, is_XSS, is_PathTraversal, is_RCE):
            case (True, _, _, _):
                attack_type = "SQL Injection"
            case (_, True, _, _):
                attack_type = "XSS"
            case (_, _, True, _):
                attack_type = "Path Traversal"
            case (_, _, _, True):
                attack_type = "Remote Code Execution"

        if attack_type:
            # if malicious behaviour is detected the request gets redirected
            if request.url.path not in ["/welcome", "/static"]:
                request_info['attack_type'] = attack_type
                request_info['attacker_id'] = 1
                request_info['cookies'] = {}

                request_dto = RequestDTO(**request_info)

                print(f"🔄 Redirecting {request.url.path} to /welcome")
                service = RequestService()
                await service.write(request_dto)
                if attack_type == "Path Traversal":
                    print("request_info['url'] : " + request_info['url'])
                    requestedFile = fakeService.getMatchingPathTraversalPath(request_info['url'])
                    print("requestedFile: " + requestedFile)
                    fakePasswdContent = fakeService.getMatchingPathTraversalFile(requestedFile)

                    return Response(content=fakePasswdContent, media_type="text/plain")

                return RedirectResponse(url="/welcome", status_code=302)

        return response
