from aiogram.types import Message

from app.handlers.utils import send_log


async def command_start_handler(message: Message) -> None:
    bot_message = "This bot was created as a test for the BobrAi company."
    await message.answer(bot_message)
    await send_log(message, bot_message)