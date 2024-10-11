from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.models import get_db, Log
from api.schemas import LogResponse, LogCreate

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/", response_model=LogResponse)
async def add_logs(log: LogCreate, db: Session = Depends(get_db)) -> LogResponse:
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
