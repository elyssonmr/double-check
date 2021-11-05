import pytest
from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from double_check.request_token.serializers import RequestTokenSerializer


@pytest.fixture
def valid_data():
    return {
        'site_name': 'double-check.com',
        'username': 'telegram_user',
        'action': 'Confirm login page'
    }


@pytest.fixture
def serializer():
    return RequestTokenSerializer()


def test_should_be_schema_instance(serializer):
    assert isinstance(serializer, Schema)


def test_should_serialize(valid_data, serializer):
    try:
        serializer.load(valid_data)
    except ValidationError:
        pytest.fail('Should not raise ValidationError')


def test_should_have_all_valid_fields(valid_data, serializer):
    serialized_data = serializer.load(valid_data)

    assert serialized_data.get('site_name') == valid_data['site_name']
    assert serialized_data.get('username') == valid_data['username']
    assert serialized_data.get('action') == valid_data['action']
