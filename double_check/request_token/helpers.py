import random
from datetime import datetime, timedelta

from double_check.cache import redis_cache
from double_check.request_token.serializers import RequestTokenSerializer


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
    await redis_cache.setex(client_token, 15, user_token)
