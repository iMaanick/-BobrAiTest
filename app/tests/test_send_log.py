from unittest.mock import patch, Mock

import aiohttp
import pytest
from aiogram.types import User, Message

from app.handlers.utils import send_log


@pytest.mark.asyncio
async def test_send_log_success() -> None:
    user = Mock(spec=User)
    user.id = 111
    message = Mock(spec=Message)
    message.text = "/start"
    message.from_user = user
    response = "This bot was created as a test for the BobrAi company."
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json.return_value = {"log_id": 1}

        await send_log(message, response)

        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"] == {
            "user_id": 111,
            "command": "/start",
            "response": "This bot was created as a test for the BobrAi company."
        }


@pytest.mark.asyncio
async def test_send_log_invalid_user() -> None:
    user = None
    message = Mock(spec=Message)
    message.text = "/start"
    message.from_user = user

    response = "This bot was created as a test for the BobrAi company."

    with patch("logging.warning") as mock_warning:
        await send_log(message, response)
        mock_warning.assert_called_once_with("Failed to add log. Invalid user or message text")


@pytest.mark.asyncio
async def test_send_log_invalid_command() -> None:
    user = Mock(spec=User)
    user.id = 111
    message = Mock(spec=Message)
    message.text = None
    message.from_user = user
    response = "This bot was created as a test for the BobrAi company."

    with patch("logging.warning") as mock_warning:
        await send_log(message, response)

        mock_warning.assert_called_once_with("Failed to add log. Invalid user or message text")


@pytest.mark.asyncio
async def test_send_log_server_error() -> None:
    user = Mock(spec=User)
    user.id = 111
    message = Mock(spec=Message)
    message.text = "/start"
    message.from_user = user
    response = "This bot was created as a test for the BobrAi company."

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 500
        mock_post.return_value.__aenter__.return_value.text.return_value = "Internal Server Error"

        with patch("logging.error") as mock_error:
            await send_log(message, response)

            mock_error.assert_called_once_with("Failed to add log. Status code: %d, Error: %s", 500,
                                               "Internal Server Error")


@pytest.mark.asyncio
async def test_send_log_http_error() -> None:
    user = Mock(spec=User)
    user.id = 111
    message = Mock(spec=Message)
    message.text = "/start"
    message.from_user = user
    response = "This bot was created as a test for the BobrAi company."

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.side_effect = aiohttp.ClientError("Connection error")

        with patch("logging.error") as mock_error:
            await send_log(message, response)

            mock_error.assert_called_once_with("HTTP request failed: %s", "Connection error")


@pytest.mark.asyncio
async def test_send_log_unexpected_error() -> None:
    user = Mock(spec=User)
    user.id = 111
    message = Mock(spec=Message)
    message.text = "/start"
    message.from_user = user
    response = "This bot was created as a test for the BobrAi company."

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.side_effect = Exception("Unexpected error")

        with patch("logging.error") as mock_error:
            await send_log(message, response)

            mock_error.assert_called_once_with("An unexpected error occurred: %s", "Unexpected error")
