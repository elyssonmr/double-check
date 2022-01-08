from unittest.mock import patch
from uuid import uuid4

import pytest

from double_check.request_token.helpers import save_token_data


@pytest.fixture
def mock_cache():
    with patch('double_check.request_token.helpers.redis_cache') as patched:
        yield patched


async def test_should_call_cache_set(mock_cache, setup_future):
    mock_cache.setex.return_value = setup_future()
    client_token = str(uuid4())
    user_token = '123456'

    await save_token_data(client_token, user_token)

    mock_cache.setex.assert_called_once_with(client_token, 15, user_token)
