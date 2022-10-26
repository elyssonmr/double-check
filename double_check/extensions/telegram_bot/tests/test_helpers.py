from unittest.mock import AsyncMock, patch

import pytest

from double_check.extensions.telegram_bot.helpers import (
    get_chat_id, send_telegram_message)


@pytest.fixture
def mock_send_message():
    with patch(
        'double_check.extensions.telegram_bot.helpers.'
        'telegram_bot.send_message'
    ) as patched:
        yield patched


@pytest.fixture
def mock_redis_cache():
    with patch(
        'double_check.extensions.telegram_bot.helpers.redis_cache'
    ) as patched:
        yield patched


async def test_should_call_telegram_send_message(mock_send_message):
    chat_id = 12345

    await send_telegram_message(
        chat_id,
        'This is your token'
    )

    mock_send_message.assert_called_once_with(
        chat_id,
        'This is your token'
    )


async def test_get_chat_id_should_call_cache_get(mock_redis_cache):
    chat_id = 12345
    username = 'darth_user'
    mock_redis_cache.get = AsyncMock(return_value=chat_id)

    response = await get_chat_id(username)

    assert response == chat_id
    mock_redis_cache.get.assert_called_once_with(username)


async def test_get_chat_id_should_return_int(
    mock_redis_cache
):
    chat_id = b'12345'
    username = 'darth_user'
    mock_redis_cache.get = AsyncMock(return_value=chat_id)

    response = await get_chat_id(username)

    assert isinstance(response, int)


async def test_get_chat_id_should_return_none_for_non_existing_chat(
    mock_redis_cache
):
    username = 'darth_user'
    mock_redis_cache.get = AsyncMock(return_value=None)

    response = await get_chat_id(username)

    assert response is None
