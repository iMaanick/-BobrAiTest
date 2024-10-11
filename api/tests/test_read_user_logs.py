from datetime import datetime, timedelta
from typing import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from api.main import app
from api.models import Base, Log, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def setup_logs(db_session: Session) -> None:
    now = datetime.utcnow()
    logs = [
        Log(user_id=1, command="/test1", timestamp=now - timedelta(days=3), response="Response 1"),
        Log(user_id=1, command="/test2", timestamp=now - timedelta(days=2), response="Response 2"),
        Log(user_id=2, command="/test3", timestamp=now - timedelta(days=1), response="Response 3"),
        Log(user_id=1, command="/test4", timestamp=now, response="Response 4"),
    ]
    db_session.add_all(logs)
    db_session.commit()


def test_read_user_logs_all(client: TestClient, setup_logs: None) -> None:
    user_id = 1
    response = client.get(f"/logs/{user_id}")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 3
    assert isinstance(logs, list)
    assert all(log["user_id"] == user_id for log in logs)


def test_read_user_logs_with_skip_and_limit(client: TestClient, setup_logs: None) -> None:
    user_id = 1
    response = client.get(f"/logs/{user_id}?skip=1&limit=1")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 1
    assert logs[0]["command"] == "/test2"


def test_read_user_logs_with_date_filter(client: TestClient, setup_logs: None) -> None:
    user_id = 1
    start_date = (datetime.utcnow() - timedelta(days=2, hours=1)).isoformat()
    end_date = datetime.utcnow().isoformat()

    response = client.get(f"/logs/{user_id}?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 2
    assert logs[0]["command"] == "/test2"
    assert logs[1]["command"] == "/test4"


def test_read_user_logs_with_invalid_date_format(client: TestClient, setup_logs: None) -> None:
    user_id = 1
    response = client.get(f"/logs/{user_id}?start_date=invalid-date")
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["query", "start_date"]
    assert data["detail"][0]["msg"] == "Input should be a valid datetime or date, invalid character in year"
    assert data["detail"][0]["type"] == "datetime_from_date_parsing"


def test_read_user_logs_no_logs(client: TestClient, setup_logs: None) -> None:
    user_id = 3
    response = client.get(f"/logs/{user_id}")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 0


def test_read_user_logs_invalid_user_id(client: TestClient, setup_logs: None) -> None:
    response = client.get("/logs/not-an-integer")
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ['path', 'user_id']
    assert data["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"
    assert data["detail"][0]["type"] == "int_parsing"


def test_read_user_logs_db_error(client: TestClient, db_session: Session, setup_logs: None) -> None:
    user_id = 1
    with patch.object(db_session, "query", side_effect=Exception("DB Error")):
        response = client.get(f"/logs/{user_id}")
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Internal Server Error"
