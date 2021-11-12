from aiohttp.web import RouteDef

from double_check.request_token.handlers import request_token

ROUTES = [
    RouteDef(
        'POST',
        r'/request_token',
        request_token,
        {'name': 'request_token'}
    )
]
