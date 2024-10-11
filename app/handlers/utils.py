import logging

import aiohttp
from aiogram.types import Message, User


async def send_log(message: Message, response: str) -> None:
    user = message.from_user
    command = message.text

    if not isinstance(user, User) or not isinstance(command, str):
        logging.warning("Failed to add log. Invalid user or message text")
        return

    url = "http://127.0.0.1:8000/logs/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "user_id": user.id,
        "command": command,
        "response": response
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    log_response = await resp.json()
                    logging.info("Log added successfully: %s", log_response)
                else:
                    error_text = await resp.text()
                    logging.error("Failed to add log. Status code: %d, Error: %s", resp.status, error_text)
    except aiohttp.ClientError as e:
        logging.error("HTTP request failed: %s", str(e))
    except Exception as e:
        logging.error("An unexpected error occurred: %s", str(e))

