import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import BotCommand
from dotenv import load_dotenv

from app.handlers.start import command_start_handler
from app.handlers.unknown_command import unknown_command_handler
from app.handlers.weather import command_weather_handler


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/weather", description="Get current weather in a specified city. Example: /weather <city>")
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token=os.environ.get("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.message.register(command_start_handler, Command("start", prefix="/"))
    dp.message.register(command_weather_handler, Command("weather", prefix="/"))
    dp.message.register(unknown_command_handler)

    await bot.set_my_description("This bot was created as a test for the BobrAi company.")
    await bot.set_my_short_description("This bot was created as a test for the BobrAi company.")
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
