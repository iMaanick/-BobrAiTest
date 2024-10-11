from unittest.mock import Mock

import pytest
from python_weather.forecast import Forecast

from app.handlers.weather import get_weather_message


@pytest.mark.asyncio
async def test_get_weather_message_returns_correct_string() -> None:
    weather = Mock(spec=Forecast)
    weather.temperature = 20
    weather.feels_like = 22
    weather.description = "Cloudy"
    weather.humidity = 70
    weather.wind_speed = 5

    message = await get_weather_message(weather)

    assert message == (
        "Temperature: 20\n"
        "Feels like: 22\n"
        "Weather description: cloudy\n"
        "Humidity: 70\n"
        "Wind speed: 5\n"
    )
