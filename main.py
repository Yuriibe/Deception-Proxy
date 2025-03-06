from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from middlewares.request_logger import RequestLoggerMiddleware
from services.request_service import RequestService
import os
app = FastAPI()

app.add_middleware(RequestLoggerMiddleware)

templates = Jinja2Templates(directory="templates")


@app.get('/')
async def main():
    return 'OK2'


@app.get("/attacker/{attacker_id}")
async def get_request(attacker_id: int, service: RequestService = Depends()):
    request_data = await service.get_request_by_id(attacker_id)
    if not request_data:
        raise HTTPException(status_code=404, detail="Request not found")

    # return request_data
    return ""


@app.get('/welcome')
async def welcome(request: Request):
    return {'msg': 'Welcome!', 'headers': request.headers}


FILES_DIRECTORY = "fakeResponses/pathTraversal/dummy/"

@app.get("/files", response_class=HTMLResponse)
async def render_html(file: str = Query(None, description="File path to retrieve")):
    """
     1. If ?file= is provided, display the content of the requested file as text (instead of downloading).
     2. If no file is provided, return the static bait HTML page.
     """

    if file:
        # Construct the full file path
        sanitized_filename = file.lstrip("/")
        file_path = os.path.join(FILES_DIRECTORY, sanitized_filename)

        # Debugging: Print the requested file path
        absolute_path = os.path.abspath(file_path)
        print(f"📂 Requested File: {file_path}")
        print(f"🔍 Absolute Path: {absolute_path}")

        # ✅ Check if the file exists before serving
        if os.path.isfile(file_path):
            print("✅ File found! Displaying content...")
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()

            return HTMLResponse(content=f"<pre>{file_content}</pre>", media_type="text/html")

        else:
            print("❌ File not found!")
            raise HTTPException(status_code=404, detail="File not found")

    # ✅ Render the bait HTML page if no file is requested
    with open("templates/pathTraversalTemplate.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, media_type="text/html")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7080)
