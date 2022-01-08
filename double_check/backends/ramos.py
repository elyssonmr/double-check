import ramos

ramos.configure({
    'notification_backend': [
        'double_check.extensions.telegram_bot.backend.'
        'TelegramBotNotificationBackend'
    ]
})
