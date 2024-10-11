import pytest

from unittest.mock import AsyncMock, patch

from app.handlers.start import command_start_handler


@pytest.mark.asyncio
async def test_start_command_handler_sends_message() -> None:
    message_mock = AsyncMock(text="/start")
    await command_start_handler(message=message_mock)
    message_mock.answer.assert_called_with("This bot was created as a test for the BobrAi company.")


@pytest.mark.asyncio
@patch("app.handlers.start.send_log")
async def test_start_command_handler_calls_send_log(mock_send_log: AsyncMock) -> None:
    message_mock = AsyncMock(text="/start")
    await command_start_handler(message=message_mock)
    message_mock.answer.assert_called_once_with("This bot was created as a test for the BobrAi company.")
    mock_send_log.assert_called_once()
