import re

from double_check.request_token.helpers import generate_user_token


def test_should_return_str():
    token = generate_user_token()

    assert isinstance(token, str)


def test_should_generate_user_token():
    token = generate_user_token()

    assert len(token) == 6
    assert re.match(r'\d+', token)
