from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Query

from api.models import Log


def filter_logs(query: Query, start_date: Optional[datetime], end_date: Optional[datetime]) -> Query:
    if start_date:
        query = query.filter(Log.timestamp >= start_date)
    if end_date:
        query = query.filter(Log.timestamp <= end_date)
    return query
