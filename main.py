from typing import Union
import time
from fastapi import FastAPI, Request
from middlewares.request_logger import RequestLoggerMiddleware

app = FastAPI()

app.add_middleware(RequestLoggerMiddleware)

@app.get('/')
async def main():
    return 'OK'

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get('/welcome')
async def welcome(request: Request):
    return {'msg': 'Welcome!', 'headers': request.headers}