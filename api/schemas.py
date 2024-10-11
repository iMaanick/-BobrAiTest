from pydantic import BaseModel, Field
from datetime import datetime


class LogCreate(BaseModel):
    user_id: int = Field(description="Telegram user id")
    command: str = Field(description="Command executed by the user")
    response: str = Field(description="Telegram bot response")


class LogResponse(BaseModel):
    id: int = Field(description="Unique identifier of the log entry")
    user_id: int = Field(description="Telegram user id")
    command: str = Field(description="Command executed by the user")
    timestamp: datetime = Field(description="Timestamp when the log was created")
    response: str = Field(description="Telegram bot response")

    class Config:
        from_attributes = True
