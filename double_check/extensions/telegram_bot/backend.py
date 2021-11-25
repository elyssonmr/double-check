from ramos.mixins import SingletonCreateMixin

from double_check.backends.notification.notification_backend import \
    NotificationBackend


class TelegramBotNotificationBackend(
    SingletonCreateMixin, NotificationBackend
):
    id = 'telegram_notification'

    async def send_token_to_customer(self, username: str, token: str):
        pass
