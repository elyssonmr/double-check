from decouple import config

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', '111:fake')
REDIS_URL = config('REDIS_URL', 'redis://localhost')
NOTIFICATION_BACKEND = config('NOTIFICATION_BACKEND', 'telegram_notification')
