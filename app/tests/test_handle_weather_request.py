from unittest.mock import AsyncMock, patch, Mock

import pytest
import python_weather
from aiogram.types import Message
from python_weather.forecast import Forecast

from app.handlers.weather import handle_weather_request


@pytest.mark.asyncio
async def test_handle_weather_request_success() -> None:
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/weather London"
    mock_message.answer = AsyncMock()
    city = "London"

    with patch("python_weather.Client") as mock_client:
        mock_weather = Mock(spec=Forecast)
        mock_weather.temperature = 20
        mock_weather.feels_like = 22
        mock_weather.description = "Cloudy"
        mock_weather.humidity = 70
        mock_weather.wind_speed = 5
        mock_client_instance = mock_client.return_value.__aenter__.return_value
        mock_client_instance.get.return_value = mock_weather
        get_message_res = (
            "Temperature: 20\n"
            "Feels like: 22\n"
            "Weather description: cloudy\n"
            "Humidity: 70\n"
            "Wind speed: 5\n"
        )
        with patch("app.handlers.weather.send_log") as mock_send_log:
            await handle_weather_request(mock_message, city)

            mock_message.answer.assert_called_once_with(get_message_res)

            mock_send_log.assert_called_once_with(mock_message, get_message_res)


@pytest.mark.asyncio
async def test_handle_weather_request_invalid_city() -> None:
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/weather UnknownCity"
    mock_message.answer = AsyncMock()
    city = "UnknownCity"

    with patch("python_weather.Client") as mock_client:
        mock_client_instance = mock_client.return_value.__aenter__.return_value
        mock_client_instance.get.side_effect = python_weather.errors.RequestError(Exception("RequestError"))

        with patch("app.handlers.weather.send_log") as mock_send_log:
            await handle_weather_request(mock_message, city)

            mock_message.answer.assert_called_once_with("/weather command error, city may be incorrect")

            mock_send_log.assert_called_once_with(mock_message, "/weather command error, city may be incorrect")


@pytest.mark.asyncio
async def test_handle_weather_request_unexpected_error() -> None:
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/weather Moscow"
    mock_message.answer = AsyncMock()
    city = "Moscow"

    with patch("python_weather.Client") as mock_client:
        mock_client_instance = mock_client.return_value.__aenter__.return_value
        mock_client_instance.get.side_effect = Exception("Unexpected error")

        with patch("app.handlers.weather.send_log") as mock_send_log:

            await handle_weather_request(mock_message, city)

            mock_message.answer.assert_called_once_with("/weather command error")
            mock_send_log.assert_called_once_with(mock_message, "/weather command error")

