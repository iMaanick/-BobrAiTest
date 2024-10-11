from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.models import get_db, Log
from api.schemas import LogResponse, LogCreate

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/", response_model=LogResponse)
async def add_logs(log: LogCreate, db: Session = Depends(get_db)) -> LogResponse:
    """
       Create a new log entry.

       This endpoint creates a new log entry with the provided user ID, command, and response.

       **Request:**
         - **Method:** POST
         - **URL:** /logs/
         - **Body:** JSON object with `user_id`, `command`, and `response` fields.
           - **Example:**
             ```json
             {
                 "user_id": 123,
                 "command": "start_process",
                 "response": "Process started successfully."
             }
             ```

       **Database Operations:**
         - Adds the new log entry to the database with the current UTC time as `timestamp`.

       **Response:**
         - Returns the created log entry as a JSON object.
           - **Example:**
             ```json
             {
                 "id": 1,
                 "user_id": 123,
                 "command": "/start",
                 "response": "This bot was created as a test for the BobrAi company.",
                 "timestamp": "2024-04-27T12:34:56Z"
             }
             ```
       """
    log_entry = Log(
        user_id=log.user_id,
        command=log.command,
        timestamp=datetime.utcnow(),
        response=log.response
    )
    try:
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return LogResponse.from_orm(log_entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
