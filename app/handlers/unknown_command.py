from aiogram.types import Message

from app.handlers.utils import send_log


async def unknown_command_handler(message: Message) -> None:
    bot_message = "Unknown command"
    await message.answer(bot_message)
    await send_log(message, bot_message)
