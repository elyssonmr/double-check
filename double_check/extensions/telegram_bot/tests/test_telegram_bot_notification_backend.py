from unittest.mock import patch

import pytest

from double_check.backends.pools.notification import NotificationPool


@pytest.fixture
def backend():
    return NotificationPool.get('telegram_notification')


@pytest.fixture
def mock_send_telegram_message():
    with patch(
        'double_check.extensions.telegram_bot.backend.send_telegram_message'
    ) as patched:
        yield patched


@pytest.fixture
def mock_get_chat_id():
    with patch(
        'double_check.extensions.telegram_bot.backend.get_chat_id'
    ) as patched:
        yield patched


async def test_send_token_should_call_send_telegram_message(
    backend,
    mock_send_telegram_message,
    mock_get_chat_id
):
    action = 'Login'
    chat_id = b'12345'
    username = 'test_username'
    token = 'token123'
    mock_get_chat_id.return_value = chat_id

    await backend.send_token_to_customer(
        action,
        username,
        token
    )

    mock_send_telegram_message.assert_called_once_with(
        chat_id,
        f'Hello {username}. Action: {action} Your token is: {token}'
    )


async def test_send_token_should_get_chat_id(
    backend,
    mock_send_telegram_message,
    mock_get_chat_id
):
    action = 'Login'
    chat_id = b'12345'
    username = 'darth_username'
    token = 'token123'
    mock_get_chat_id.return_value = chat_id

    await backend.send_token_to_customer(
        action,
        username,
        token
    )

    mock_get_chat_id.assert_called_once_with(username)


async def test_send_token_should_rise_exeception_when_user_does_not_exists(
    backend,
    mock_send_telegram_message,
    mock_get_chat_id
):
    username = 'darth_username'
    token = 'token123'
    mock_get_chat_id.return_value = None

    with pytest.raises(Exception):
        await backend.send_token_to_customer(
            username,
            token
        )

    mock_send_telegram_message.assert_not_called()
