from fastapi import Request


async def extract_request_data(request: Request) -> dict:
    request_data = {
        "method": request.method if request.method else None,
        "url": str(request.url) if request.url else None,
        "user-agent": request.headers.get("user-agent", None),
        "sec-ch-ua": request.headers.get("sec-ch-ua", None),
        "sec-ch-ua-platform": request.headers.get("sec-ch-ua-platform", None),
        "host": request.headers.get("host", None),
        "client-ip": request.client.host if request.client.host else None,
        "cookies": request.cookies if request.cookies else None
    }

    return request_data
