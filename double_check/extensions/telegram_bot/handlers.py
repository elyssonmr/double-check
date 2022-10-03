from aiogram import Dispatcher, types
from aiogram.types.message import ParseMode
from aiogram.utils import markdown
import aioredis

from double_check.cache import redis_cache
from double_check.extensions.telegram_bot.bot import telegram_bot

from double_check import config

dispatcher = Dispatcher(telegram_bot)
redis_client = aioredis.from_url(config.REDIS_URL)


@dispatcher.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    username = message.from_user.username
    if not username:
        username_link = markdown.link(
            'https://telegram.org/blog/usernames-and-secret-chats-v2',
            'https://telegram.org/blog/usernames-and-secret-chats-v2'
        )
        no_username_message = (
            f'Ops... Could not identify your {markdown.italic("username")}.\n'
            f'We need an {markdown.italic("username")} to be set in other to '
            'start using the bot.\n'
            'This link could help you setting your username: '
            f'{username_link}\n'
            f'After setup your username just type {markdown.bold("/start")}'
        )
        await message.answer(
            no_username_message,
            parse_mode=ParseMode.MARKDOWN
        )
        return

    chat_id = message.chat.id
    await redis_cache.set(username, chat_id)
    greetings = (
        f'Hello {markdown.bold(username)}!!\n'
        f'Thank you for using {markdown.bold("Double Check Bot")}!\n'
        'You are going to receive a token as soon as an application request '
        'a new token to Double Check you :)'
    )
    await message.answer(greetings, parse_mode=ParseMode.MARKDOWN)


@dispatcher.message_handler(commands=['stop', 'exit'])
async def stop_handler(message: types.Message):
    username = message.from_user.username
    if username:
        await redis_cache.delete(username)

    stop_message = (
        'I\'ll miss you :(\n'
        f'If you change your mind just type {markdown.bold("/start")} again'
    )
    await message.answer(stop_message, parse_mode=ParseMode.MARKDOWN)
