from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter
from middlewares.request_logger import RequestLoggerMiddleware
from services.request_service import RequestService

app = FastAPI()

app.add_middleware(RequestLoggerMiddleware)


@app.get('/')
async def main():
    return 'OK'


@app.get("/attacker/{attacker_id}")
async def get_request(attacker_id: int, service: RequestService = Depends()):
    request_data = await service.get_request_by_id(attacker_id)
    if not request_data:
        raise HTTPException(status_code=404, detail="Request not found")

    return request_data


@app.get('/welcome')
async def welcome(request: Request):
    return {'msg': 'Welcome!', 'headers': request.headers}
