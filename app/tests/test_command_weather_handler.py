from unittest.mock import patch, AsyncMock

import pytest
from aiogram.filters import CommandObject
from aiogram.types import Message

from app.handlers.weather import command_weather_handler


@pytest.mark.asyncio
@patch("app.handlers.weather.send_log")
async def test_command_weather_handler_no_city(mock_send_log: AsyncMock) -> None:
    message = AsyncMock(spec=Message)
    message.text = "/weather"
    message.answer = AsyncMock()
    command = CommandObject(args="")

    await command_weather_handler(message, command)

    message.answer.assert_called_once_with("City not specified")
    mock_send_log.assert_called_once_with(message, "City not specified")


@pytest.mark.asyncio
@patch("app.handlers.weather.send_log")
async def test_command_weather_handler_invalid_input(mock_send_log: AsyncMock) -> None:
    message = AsyncMock(spec=Message)
    message.text = "/weather Moscow Tver"
    message.answer = AsyncMock()
    command = CommandObject(args="Moscow Tver")

    await command_weather_handler(message, command)

    message.answer.assert_called_once_with("Invalid input format")
    mock_send_log.assert_called_once_with(message, "Invalid input format")


@pytest.mark.asyncio
@patch("app.handlers.weather.handle_weather_request")
async def test_command_weather_handler_valid_city(mock_handle_weather_request: AsyncMock) -> None:
    message = AsyncMock(spec=Message)
    message.text = "/weather Moscow"
    message.answer = AsyncMock()
    command = CommandObject(args="Moscow")

    await command_weather_handler(message, command)

    mock_handle_weather_request.assert_called_once_with(message, "Moscow")
