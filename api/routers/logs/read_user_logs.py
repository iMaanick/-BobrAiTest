from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.models import get_db, Log
from api.routers.utils import filter_logs
from api.schemas import LogResponse

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/{user_id}", response_model=List[LogResponse])
async def read_user_logs(
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        db: Session = Depends(get_db)
) -> List[LogResponse]:
    try:
        query = db.query(Log).filter(Log.user_id == user_id)
        query = filter_logs(query, start_date, end_date)

        logs = query.offset(skip).limit(limit).all()
        return [LogResponse.from_orm(log) for log in logs]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")