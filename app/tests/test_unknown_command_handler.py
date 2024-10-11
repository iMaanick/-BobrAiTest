import pytest

from unittest.mock import AsyncMock, patch

from app.handlers.unknown_command import unknown_command_handler


@pytest.mark.asyncio
async def test_unknown_command_handler_sends_message() -> None:
    message_mock = AsyncMock(text="test123")
    await unknown_command_handler(message=message_mock)
    message_mock.answer.assert_called_with("Unknown command")


@pytest.mark.asyncio
@patch("app.handlers.unknown_command.send_log")
async def test_unknown_command_handler_calls_send_log(mock_send_log: AsyncMock) -> None:
    message_mock = AsyncMock(text="test123")
    await unknown_command_handler(message=message_mock)
    message_mock.answer.assert_called_with("Unknown command")
    mock_send_log.assert_called_once()
