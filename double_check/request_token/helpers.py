from datetime import datetime, timedelta
from uuid import uuid4

from double_check.request_token.serializers import RequestTokenSerializer


def validate_request_token_data(request_body: dict) -> dict:
    return RequestTokenSerializer().load(request_body)


def create_response() -> dict:
    ttl = datetime.utcnow() + timedelta(seconds=15)

    return {
        'token': str(uuid4()),
        'ttl': ttl.strftime('%Y-%m-%d %H:%M:%S')
    }
