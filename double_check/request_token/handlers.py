import json
from json.decoder import JSONDecodeError

from aiohttp.web import Request, Response, StreamResponse
from aiohttp.web_exceptions import HTTPBadRequest

from double_check.request_token.helpers import validate_request_token_data


async def request_token(request: Request) -> StreamResponse:
    try:
        request_body = await request.json()
    except JSONDecodeError:
        raise HTTPBadRequest(
            text=json.dumps({'error': 'Invalid Json'}),
            content_type='application/json'
        )

    validate_request_token_data(request_body)
    return Response()
