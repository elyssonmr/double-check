from ramos.mixins import SingletonCreateMixin

from double_check.backends.notification.notification_backend import \
    NotificationBackend
from double_check.extensions.telegram_bot.bot import telegram_bot
from double_check.extensions.telegram_bot.helpers import (
    get_chat_id, send_telegram_message)


class TelegramBotNotificationBackend(
    SingletonCreateMixin, NotificationBackend
):
    id = 'telegram_notification'

    async def send_token_to_customer(self, username: str, token: str):
        chat_id = await get_chat_id(username)
        if not chat_id:
            updates = await telegram_bot.get_updates()
            for update in updates:
                if update['from']['username'] == username:
                    chat_id = updates['chat']['id']
        if not chat_id:
            raise Exception()

        message = f'Hello {username}. Your token is: {token}'

        await send_telegram_message(chat_id, message)
