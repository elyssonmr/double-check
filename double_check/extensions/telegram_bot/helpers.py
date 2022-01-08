from double_check.cache import redis_cache
from double_check.extensions.telegram_bot.bot import telegram_bot


async def send_telegram_message(chat_id: int, message: str):
    await telegram_bot.send_message(
        chat_id, message)


async def get_chat_id(username: str):
    chat_id = await redis_cache.get(username)

    return int(chat_id) if chat_id else chat_id
