import random
from datetime import datetime, timedelta

from double_check.cache import redis_cache
from double_check.request_token.serializers import (CheckTokenSerializer,
                                                    RequestTokenSerializer)


def validate_request_token_data(request_body: dict) -> dict:
    return RequestTokenSerializer().load(request_body)


def create_response(token: str) -> dict:
    ttl = datetime.utcnow() + timedelta(seconds=15)

    return {
        'token': str(token),
        'ttl': ttl.strftime('%Y-%m-%d %H:%M:%S')
    }


def generate_user_token() -> str:
    chars = [str(i) for i in range(10)]
    return ''.join(random.choices(chars, k=6))


async def save_token_data(client_token: str, user_token: str) -> None:
    await redis_cache.setex(client_token, 60, user_token)


def validate_check_token_data(request_body: dict) -> dict:
    return CheckTokenSerializer().load(request_body)


async def verify_token(client_token: str, user_token: str) -> bool:
    token = await redis_cache.get(client_token)

    if token:
        return token.decode('utf-8') == user_token

    return False
