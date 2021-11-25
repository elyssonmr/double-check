from unittest.mock import patch

import pytest

from double_check.extensions.telegram_bot.helpers import send_telegram_message


@pytest.fixture
def mock_send_message():
    with patch(
        'double_check.extensions.telegram_bot.helpers.'
        'telegram_bot.send_message'
    ) as patched:
        yield patched


async def test_should_call_telegram_send_message(
    mock_send_message,
    setup_future
):
    mock_send_message.return_value = setup_future()

    await send_telegram_message(
        12345,
        'This is your token'
    )

    mock_send_message.assert_called_once_with(
        12345,
        'This is your token'
    )
