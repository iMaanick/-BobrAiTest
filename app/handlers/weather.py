import logging

import python_weather
from aiogram.filters import CommandObject
from aiogram.types import Message
from python_weather.forecast import Forecast

from app.handlers.utils import send_log


async def get_weather_message(weather: Forecast) -> str:
    return (f"Temperature: {weather.temperature}\n"
            f"Feels like: {weather.feels_like}\n"
            f"Weather description: {weather.description.lower()}\n"
            f"Humidity: {weather.humidity}\n"
            f"Wind speed: {weather.wind_speed}\n")


async def handle_weather_request(message: Message, city: str) -> None:
    async with python_weather.Client(unit=python_weather.METRIC, locale=python_weather.enums.Locale.ENGLISH) as client:
        try:
            weather = await client.get(location=city)
            bot_message = await get_weather_message(weather)
            await message.answer(bot_message)
            await send_log(message, bot_message)
        except python_weather.errors.RequestError:
            bot_message = "/weather command error, city may be incorrect"
            await message.answer(bot_message)
            await send_log(message, bot_message)
        except Exception as e:
            logging.error("An unexpected error occurred: %s", str(e))
            bot_message = "/weather command error"
            await message.answer(bot_message)
            await send_log(message, bot_message)


async def command_weather_handler(message: Message, command: CommandObject) -> None:
    city = command.args.strip() if command.args else None

    if not city:
        bot_message = "City not specified"
        await message.answer(bot_message)
        await send_log(message, bot_message)
        return

    if len(city.split()) > 1:
        bot_message = "Invalid input format"
        await message.answer(bot_message)
        await send_log(message, bot_message)
        return

    await handle_weather_request(message, city)
