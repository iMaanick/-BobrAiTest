from typing import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from api.main import app
from api.models import Base, get_db

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


def test_add_logs_success(client: TestClient) -> None:
    log_data = {
        "user_id": 1,
        "command": "/test",
        "response": "Test response"
    }

    response = client.post("/logs/", json=log_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == log_data["user_id"]
    assert data["command"] == log_data["command"]
    assert data["response"] == log_data["response"]
    assert "id" in data
    assert "timestamp" in data


def test_add_logs_missing_fields(client: TestClient) -> None:
    log_data = {
        "user_id": 1,
        "command": "/test"
        # no "response" field
    }

    response = client.post("/logs/", json=log_data)
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "response"]
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["type"] == "missing"


def test_add_logs_invalid_data(client: TestClient) -> None:
    log_data = {
        "user_id": "not_an_integer",
        "command": "/test",
        "response": "Test response"
    }

    response = client.post("/logs/", json=log_data)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "user_id"]
    assert data["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"
    assert data["detail"][0]["type"] == "int_parsing"


def test_add_logs_db_error(client: TestClient, db_session: Session) -> None:
    log_data = {
        "user_id": 1,
        "command": "/test",
        "response": "Test response"
    }

    with patch.object(db_session, "commit", side_effect=Exception("DB Commit Error")):
        response = client.post("/logs/", json=log_data)
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Internal Server Error"

