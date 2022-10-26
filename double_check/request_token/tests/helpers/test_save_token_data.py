from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from double_check.request_token.helpers import save_token_data


@pytest.fixture
def mock_cache():
    with patch('double_check.request_token.helpers.redis_cache') as patched:
        yield patched


async def test_should_call_cache_set(mock_cache):
    mock_cache.setex = AsyncMock()
    client_token = str(uuid4())
    user_token = '123456'

    await save_token_data(client_token, user_token)

    mock_cache.setex.assert_called_once_with(client_token, 60, user_token)
