from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.models import get_db, Log
from api.routers.utils import filter_logs
from api.schemas import LogResponse

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/", response_model=List[LogResponse])
async def read_logs(
        skip: int = 0,
        limit: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        db: Session = Depends(get_db)
) -> List[LogResponse]:
    """
    Retrieve log entries.

    This endpoint retrieves a list of log entries from the database. It supports pagination through `skip` and `limit` parameters and allows filtering logs within a specific date range using `start_date` and `end_date`.

    **Request:**
      - **Method:** GET
      - **URL:** /logs/
      - **Query Parameters:**
        - **skip** (integer, optional, default=0): Number of records to skip for pagination.
        - **limit** (integer, optional, default=10): Maximum number of records to return.
        - **start_date** (ISO 8601 datetime, optional): Filter logs created after this date and time.
        - **end_date** (ISO 8601 datetime, optional): Filter logs created before this date and time.
      - **Example:**
        ```
        GET /logs/?skip=0&limit=5&start_date=2024-01-01T00:00:00Z&end_date=2024-12-31T23:59:59Z
        ```

    **Database Operations:**
      - Queries the `logs` table, optionally filtering by `start_date` and `end_date`.
      - Applies pagination using `skip` and `limit`.
      - Retrieves the filtered and paginated list of logs.

    **Response:**
      - Returns a list of log entries as JSON objects.
        - **Example:**
          ```json
          [
              {
                  "id": 1,
                  "user_id": 123,
                  "command": "/start",
                  "response": "This bot was created as a test for the BobrAi company.",
                  "timestamp": "2024-04-27T12:34:56Z"
              },
              {
                  "id": 2,
                  "user_id": 456,
                  "command": "/start",
                  "response": "This bot was created as a test for the BobrAi company.",
                  "timestamp": "2024-04-28T09:15:30Z"
              }
          ]
          ```
    """
    try:

        query = db.query(Log)
        query = filter_logs(query, start_date, end_date)

        logs = query.offset(skip).limit(limit).all()
        return [LogResponse.from_orm(log) for log in logs]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")