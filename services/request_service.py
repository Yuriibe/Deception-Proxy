from database.db import *

class RequestService:
    def __init__(self):
        self.repository = RequestRepository()

    async def get_request_by_id(self, request_id: int):

        request_data = await self.repository.get_request_by_id(request_id)

        if request_data:
           request_data["user_agent"] = "[REDACTED]"

        return request_data

    async def write(self):
        print("write")
        await self.repository.write_to_table("request_header", {
            "method": "GET",
            "url": "http://malicious.com/login",
            "user_agent": "Mozilla/5.0",
            "sec_ch_ua": None,
            "sec_ch_ua_platform": "Windows",
            "client_ip": "192.168.1.10",
            "cookies": "sessionid=abc123",
            "attack_type": "SQL Injection",
            "attacker_id": 4
        })
        return True
