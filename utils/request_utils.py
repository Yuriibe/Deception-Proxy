from fastapi import Request

async def extract_request_data(request: Request) -> dict:
    request_data = {
        "method": request.method if request.method else None,
        "url": str(request.url) if request.url else None,
        "user_agent": request.headers.get("user-agent", None),
        "sec_ch_ua": request.headers.get("sec-ch-ua", None),
        "sec_ch_ua_platform": request.headers.get("sec-ch-ua-platform", None),
        # "host": request.headers.get("host", None),
        "client_ip": request.client.host if request.client.host else None,
        "cookies": request.cookies if request.cookies else None,
        "attack_type": "",
        "attacker_id": None
    }

    return request_data

