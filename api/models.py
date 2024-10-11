import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from datetime import datetime

load_dotenv()
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./logs.db")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    command = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response = Column(String)


Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
