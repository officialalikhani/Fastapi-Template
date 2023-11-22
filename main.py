from fastapi import FastAPI, HTTPException
from database.main import MongoDb
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from security.auth import *
from routes.auth_route import router as routes_auth
from routes.sample_route import router as routes_sample
import logging
from logging.handlers import RotatingFileHandler
import uvicorn

mg = MongoDb()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = RotatingFileHandler("app.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

app.include_router(routes_auth)
app.include_router(routes_sample)


@app.exception_handler(HTTPException)
async def handle_http_exception(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": "Not authenticated", "data": ""},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port="Your-Port", workers="", reload=True)
