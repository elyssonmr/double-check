from ramos.mixins import SingletonCreateMixin

from double_check.backends.notification.notification_backend import \
    NotificationBackend
from double_check.extensions.telegram_bot.helpers import (
    get_chat_id, send_telegram_message)


class TelegramBotNotificationBackend(
    SingletonCreateMixin, NotificationBackend
):
    id = 'telegram_notification'

    async def send_token_to_customer(
            self,
            action: str,
            username: str,
            token: str
    ):
        chat_id = await get_chat_id(username)
        if not chat_id:
            raise Exception()

        message = f'Hello {username}. Action: {action} Your token is: {token}'

        await send_telegram_message(chat_id, message)
