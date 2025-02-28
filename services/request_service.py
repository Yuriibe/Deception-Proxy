from database.db import *
from dto.request_dto import RequestDTO

class RequestService:
    def __init__(self):
        self.repository = RequestRepository()

    async def get_request_by_id(self, request_id: int):

        request_data = await self.repository.get_request_by_id(request_id)

        if request_data:
           request_data["user_agent"] = "[REDACTED]"

        return request_data

    async def write(self, request_data: RequestDTO):
        await self.repository.write_to_table("request_header", request_data.dict())
        return True
