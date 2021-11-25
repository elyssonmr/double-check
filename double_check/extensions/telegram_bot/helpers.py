from double_check.extensions.telegram_bot.bot import telegram_bot


async def send_telegram_message(chat_id: int, message: str):
    await telegram_bot.send_message(
        chat_id, message)
