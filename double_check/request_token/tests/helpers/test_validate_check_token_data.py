from uuid import uuid4
import pytest
from marshmallow.exceptions import ValidationError

from double_check.request_token.helpers import validate_check_token_data


@pytest.fixture
def valid_data():
    return {
        'request_token': str(uuid4()),
        'user_token': '123456'
    }


@pytest.fixture
def invalid_data():
    return {
        'invalid_field1': 'Double Check Request Token',
        'invalid_field2': 'double_check_user_token'
    }


def test_should_return_dict(valid_data):
    response = validate_check_token_data(valid_data)

    assert isinstance(response, dict)


def test_invalid_data_should_rise_validation_error(invalid_data):
    with pytest.raises(ValidationError) as exp:
        validate_check_token_data(invalid_data)

    errors = exp.value.messages
    assert 'request_token' in errors
    assert 'user_token' in errors
