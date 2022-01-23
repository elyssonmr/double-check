from unittest.mock import patch
from uuid import uuid4

import pytest
from aiohttp.web import Application

from double_check.request_token.handlers import check_token


@pytest.fixture
def http_client(aiohttp_client, loop):
    app = Application()
    app.router.add_post('/', check_token)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def valid_data():
    return {
        'token': str(uuid4()),
        'user_token': '123456'
    }


@pytest.fixture
def patch_validate_data():
    with patch(
        'double_check.request_token.handlers.validate_check_token_data'
    ) as patched:
        yield patched


@pytest.fixture
def patch_verify_token():
    with patch(
        'double_check.request_token.handlers.verify_token'
    ) as patched:
        yield patched


async def test_should_return_json_with_status_200(
    http_client,
    valid_data,
    patch_validate_data,
    patch_verify_token,
    setup_future
):
    patch_validate_data.return_value = valid_data
    patch_verify_token.return_value = setup_future(True)

    response = await http_client.post('/', json=valid_data)

    assert response.status == 200
    assert 'application/json' in response.headers['Content-Type']


async def test_should_raise_bad_request_for_invalid_json(http_client):
    response = await http_client.post('/')

    assert response.status == 400
    assert await response.json() == {'error': 'Invalid Json'}


async def test_should_serialize_valid_data(
    http_client,
    valid_data,
    patch_validate_data,
    patch_verify_token,
    setup_future
):
    patch_validate_data.return_value = valid_data
    patch_verify_token.return_value = setup_future(True)

    response = await http_client.post('/', json=valid_data)

    assert response.status == 200
    patch_validate_data.assert_called_once_with(valid_data)


async def test_should_verify_token(
    http_client,
    valid_data,
    patch_validate_data,
    patch_verify_token,
    setup_future
):
    patch_validate_data.return_value = valid_data
    patch_verify_token.return_value = setup_future(True)

    response = await http_client.post('/', json=valid_data)

    assert response.status == 200
    patch_verify_token.assert_called_once_with(
        valid_data['token'],
        valid_data['user_token']
    )


@pytest.mark.parametrize('valid_token', (True, False))
async def test_should_check_token(
    http_client,
    valid_data,
    patch_validate_data,
    patch_verify_token,
    setup_future,
    valid_token
):
    patch_validate_data.return_value = valid_data
    patch_verify_token.return_value = setup_future(valid_token)

    response = await http_client.post('/', json=valid_data)

    assert response.status == 200
    patch_verify_token.assert_called_once_with(
        valid_data['token'],
        valid_data['user_token']
    )
    response_body = await response.json()
    assert response_body == {
        'token': valid_data['token'],
        'is_valid': valid_token
    }
