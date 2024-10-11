from pydantic import BaseModel
from datetime import datetime


class LogCreate(BaseModel):
    user_id: int
    command: str
    response: str


class LogResponse(BaseModel):
    id: int
    user_id: int
    command: str
    timestamp: datetime
    response: str

    class Config:
        from_attributes = True

