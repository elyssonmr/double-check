from uuid import uuid4
import pytest
from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from double_check.request_token.serializers import CheckTokenSerializer


@pytest.fixture
def valid_data():
    return {
        'token': str(uuid4()),
        'user_token': '123456'
    }


@pytest.fixture
def serializer():
    return CheckTokenSerializer()


def test_should_be_schema_instance(serializer):
    assert isinstance(serializer, Schema)


def test_should_serialize(valid_data, serializer):
    try:
        serializer.load(valid_data)
    except ValidationError:
        pytest.fail('Should not raise ValidationError')


def test_should_have_all_valid_fields(valid_data, serializer):
    serialized_data = serializer.load(valid_data)

    assert serialized_data.get('token') == valid_data['token']
    assert serialized_data.get('user_token') == valid_data['user_token']
