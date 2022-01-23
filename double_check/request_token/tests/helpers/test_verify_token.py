from unittest.mock import patch
from uuid import uuid4

import pytest

from double_check.request_token.helpers import verify_token


@pytest.fixture
def mock_cache():
    with patch('double_check.request_token.helpers.redis_cache') as patched:
        yield patched


async def test_should_call_redis_get(mock_cache, setup_future):
    mock_cache.get.return_value = setup_future()
    client_token = str(uuid4())

    await verify_token(client_token, '123456')

    mock_cache.get.assert_called_once_with(client_token)


async def test_should_compare_token(mock_cache, setup_future):
    user_token = '123456'
    mock_cache.get.return_value = setup_future(user_token.encode())
    client_token = str(uuid4())

    response = await verify_token(client_token, user_token)

    assert response is True


async def test_should_not_compare_token(mock_cache, setup_future):
    user_token = '123456'
    mock_cache.get.return_value = setup_future()
    client_token = str(uuid4())

    response = await verify_token(client_token, user_token)

    assert response is False


async def test_should_compare_different_tokens(mock_cache, setup_future):
    user_token = '123456'
    mock_cache.get.return_value = setup_future('654321'.encode())
    client_token = str(uuid4())

    response = await verify_token(client_token, user_token)

    assert response is False
