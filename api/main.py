from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.logs.add_logs import router as add_logs_router
from api.routers.logs.read_logs import router as read_logs_router
from api.routers.logs.read_user_logs import router as read_user_logs_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(add_logs_router)
app.include_router(read_logs_router)
app.include_router(read_user_logs_router)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to the API!"}
