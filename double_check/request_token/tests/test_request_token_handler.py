from unittest.mock import Mock, patch

import pytest
from aiohttp.web import Application
from marshmallow.exceptions import ValidationError

from double_check import config
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
def invalid_data():
    return {
        'invalid': 'data'
    }


@pytest.fixture
def patch_validate_data():
    with patch(
        'double_check.request_token.handlers.validate_request_token_data'
    ) as patched:
        yield patched


@pytest.fixture
def mock_notification_backend():
    return Mock()


@pytest.fixture(autouse=True)
def patch_notification_pool(mock_notification_backend):
    with patch(
        'double_check.request_token.handlers.NotificationPool'
    ) as patched:
        patched.get.return_value = mock_notification_backend
        yield patched


@pytest.fixture
def patch_send_token_to_customer(mock_notification_backend):
    return mock_notification_backend.send_token_to_customer


@pytest.fixture
def patch_save_token_data():
    with patch(
        'double_check.request_token.handlers.save_token_data'
    ) as patched:
        yield patched


@pytest.fixture
def client_token():
    return '9e7b6e1e-c6ef-4ba8-bdc8-bad658d157df'


@pytest.fixture(autouse=True)
def mock_uuid4(client_token):
    with patch('double_check.request_token.handlers.uuid4') as patched:
        patched.return_value = client_token
        yield patched


@pytest.fixture
def user_token():
    return '123456'


@pytest.fixture(autouse=True)
def patch_generate_user_token(user_token):
    with patch(
        'double_check.request_token.handlers.generate_user_token'
    ) as patched:
        patched.return_value = user_token
        yield patched


async def test_should_accept_valid_json(
    http_client,
    valid_data,
    patch_save_token_data,
    patch_send_token_to_customer,
    setup_future
):
    patch_save_token_data.return_value = setup_future()
    patch_send_token_to_customer.return_value = setup_future()
    response = await http_client.post('/', json=valid_data)
    assert response.status == 202


async def test_should_raise_bad_request_for_invalid_json(http_client):
    response = await http_client.post('/')

    assert response.status == 400
    assert await response.json() == {'error': 'Invalid Json'}


async def test_should_serialize_valid_data(
    http_client,
    valid_data,
    patch_validate_data,
    patch_save_token_data,
    patch_send_token_to_customer,
    setup_future
):
    patch_save_token_data.return_value = setup_future()
    patch_send_token_to_customer.return_value = setup_future()
    response = await http_client.post('/', json=valid_data)

    assert response.status == 202
    patch_validate_data.assert_called_once_with(valid_data)


async def test_should_return_bad_request_invalid_data(
    http_client,
    invalid_data,
    patch_validate_data,
    patch_save_token_data,
    patch_send_token_to_customer
):
    patch_validate_data.side_effect = ValidationError({
        'invalid': [
            'Unknown field.'
        ]
    })
    response = await http_client.post('/', json=invalid_data)

    assert response.status == 400
    expected_response = {
        'error': 'Invalid Data',
        'errors': {
            'invalid': [
                'Unknown field.'
            ]
        }
    }
    assert await response.json() == expected_response
    patch_validate_data.assert_called_once_with(invalid_data)
    patch_send_token_to_customer.assert_not_called()


async def test_should_respond_json(
    http_client,
    valid_data,
    patch_save_token_data,
    patch_send_token_to_customer,
    setup_future
):
    patch_save_token_data.return_value = setup_future()
    patch_send_token_to_customer.return_value = setup_future()
    response = await http_client.post('/', json=valid_data)

    assert response.status == 202
    assert 'application/json' in response.headers['Content-Type']
    assert await response.json()


async def test_should_call_mocks_correctly(
    http_client,
    valid_data,
    patch_save_token_data,
    patch_send_token_to_customer,
    setup_future,
    patch_notification_pool,
    client_token,
    user_token
):
    patch_save_token_data.return_value = setup_future()
    patch_send_token_to_customer.return_value = setup_future()

    await http_client.post('/', json=valid_data)

    patch_notification_pool.get.assert_called_once_with(
        config.NOTIFICATION_BACKEND
    )
    patch_save_token_data.assert_called_once_with(
        client_token, user_token
    )
    patch_send_token_to_customer.assert_called_once_with(
        valid_data['username'],
        user_token
    )
