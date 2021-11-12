import pytest
from marshmallow.exceptions import ValidationError

from double_check.request_token.helpers import validate_request_token_data


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
        'invalid_field1': 'Double Check Login',
        'invalid_field2': 'double_check_username'
    }


def test_should_return_dict(valid_data):
    response = validate_request_token_data(valid_data)

    assert isinstance(response, dict)


def test_should_return_default_value(valid_data):
    del valid_data['action']
    response = validate_request_token_data(valid_data)

    assert 'action' in response
    assert response['action'] == 'Login'


def test_invalid_data_should_rise_validation_error(invalid_data):
    with pytest.raises(ValidationError) as exp:
        validate_request_token_data(invalid_data)

    errors = exp.value.messages
    assert 'site_name' in errors
    assert 'username' in errors
