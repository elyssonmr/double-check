import ramos


def configure_ramos() -> None:
    ramos.configure({
        'notification_backend': [
            'double_check.extensions.telegram_bot.backend.'
            'TelegramBotNotificationBackend'
        ]
    })
