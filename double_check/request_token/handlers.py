import json
from json.decoder import JSONDecodeError
from uuid import uuid4

from aiohttp.web import json_response, Request, StreamResponse
from aiohttp.web_exceptions import HTTPBadRequest

from double_check import config
from double_check.backends.pools.notification import NotificationPool
from double_check.request_token.helpers import (create_response,
                                                generate_user_token,
                                                save_token_data,
                                                validate_check_token_data,
                                                validate_request_token_data,
                                                verify_token)


async def request_token(request: Request) -> StreamResponse:
    try:
        request_body = await request.json()
    except JSONDecodeError:
        raise HTTPBadRequest(
            text=json.dumps({'error': 'Invalid Json'}),
            content_type='application/json'
        )

    request_data = validate_request_token_data(request_body)
    username = request_data['username']
    user_token = generate_user_token()
    client_token = str(uuid4())
    backend = NotificationPool.get(config.NOTIFICATION_BACKEND)
    await save_token_data(client_token, user_token)
    await backend.send_token_to_customer(username, user_token)
    token_response = create_response(client_token)
    return json_response(data=token_response, status=202)


async def check_token(request: Request) -> StreamResponse:
    try:
        request_body = await request.json()
    except JSONDecodeError:
        raise HTTPBadRequest(
            text=json.dumps({'error': 'Invalid Json'}),
            content_type='application/json'
        )

    request_data = validate_check_token_data(request_body)

    request_token = request_data['token']
    user_token = request_data['user_token']

    is_valid = await verify_token(request_token, user_token)

    response = {
        'token': request_token,
        'is_valid': is_valid
    }

    return json_response(data=response)
