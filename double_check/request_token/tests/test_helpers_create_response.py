import re
from datetime import datetime

from double_check.request_token.helpers import create_response


def test_should_return_dict():
    response = create_response()

    assert isinstance(response, dict)


def test_should_return_request_token_fields():
    response = create_response()

    assert 'token' in response
    assert 'ttl' in response


def test_should_return_token_as_uuid():
    response = create_response()

    assert re.match((
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-'
        r'[089ab][0-9a-f]{3}-[0-9a-f]{12}$'),
        response['token'])


def test_should_return_ttl_as_datetime_str():
    response = create_response()
    ttl = response['ttl']

    assert isinstance(ttl, str)
    assert datetime.strptime(ttl, '%Y-%m-%d %H:%M:%S')


def test_should_return_ttl_in_the_future():
    response = create_response()
    ttl = datetime.strptime(response['ttl'], '%Y-%m-%d %H:%M:%S')

    assert datetime.utcnow() < ttl
