from database.db import *

class RequestService:
    def __init__(self):
        self.repository = RequestRepository()

    async def get_request_by_id(self, request_id: int):

        request_data = await self.repository.get_request_by_id(request_id)

        if request_data:
           # request_data["user_agent"] = "[REDACTED]"
            print("test")
        return request_data
