from unittest.mock import patch

import pytest
from aiohttp.web import Application

from double_check.request_token.handlers import request_token


@pytest.fixture
def http_client(aiohttp_client, loop):
    app = Application()
    app.router.add_post('/', request_token)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def valid_data():
    return {
        'site_name': 'Double Check Login',
        'username': 'double_check_username',
        'action': 'Login Website'
    }


@pytest.fixture
def patch_validate_data():
    with patch(
        'double_check.request_token.handlers.validate_request_token_data'
    ) as patched:
        yield patched


async def test_should_accept_valid_json(http_client, valid_data):
    response = await http_client.post('/', json=valid_data)
    assert response.status == 200


async def test_should_raise_bad_request_for_invalid_json(http_client):
    response = await http_client.post('/')

    assert response.status == 400
    assert await response.json() == {'error': 'Invalid Json'}


async def test_should_serialize_valid_data(
    http_client,
    valid_data,
    patch_validate_data
):
    response = await http_client.post('/', json=valid_data)

    assert response.status == 200
    patch_validate_data.assert_called_once_with(valid_data)
