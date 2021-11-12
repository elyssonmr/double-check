import json
from json.decoder import JSONDecodeError

from aiohttp.web import json_response, Request, StreamResponse
from aiohttp.web_exceptions import HTTPBadRequest

from double_check.request_token.helpers import (create_response,
                                                validate_request_token_data)


async def request_token(request: Request) -> StreamResponse:
    try:
        request_body = await request.json()
    except JSONDecodeError:
        raise HTTPBadRequest(
            text=json.dumps({'error': 'Invalid Json'}),
            content_type='application/json'
        )

    validate_request_token_data(request_body)
    token_response = create_response()
    return json_response(data=token_response, status=202)
