import asyncio
import logging

import uvloop
from aiogram import executor

from double_check.extensions.telegram_bot.handlers import dispatcher

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    uvloop.install()
    loop = asyncio.get_event_loop()
    print('Starting bot')
    executor.start_polling(dispatcher, loop=loop)
