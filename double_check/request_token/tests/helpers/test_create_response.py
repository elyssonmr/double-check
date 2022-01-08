from datetime import datetime
from uuid import uuid4

import pytest

from double_check.request_token.helpers import create_response


@pytest.fixture
def token():
    return str(uuid4())


def test_should_return_dict(token):
    response = create_response(token)

    assert isinstance(response, dict)


def test_should_return_request_token_fields(token):
    response = create_response(token)

    assert 'token' in response
    assert 'ttl' in response


def test_should_return_token_arg_token(token):
    response = create_response(token)

    assert response['token'] == token


def test_should_return_ttl_as_datetime_str(token):
    response = create_response(token)
    ttl = response['ttl']

    assert isinstance(ttl, str)
    assert datetime.strptime(ttl, '%Y-%m-%d %H:%M:%S')


def test_should_return_ttl_in_the_future(token):
    response = create_response(token)
    ttl = datetime.strptime(response['ttl'], '%Y-%m-%d %H:%M:%S')

    assert datetime.utcnow() < ttl
