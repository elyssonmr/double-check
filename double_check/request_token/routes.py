from aiohttp.web import RouteDef

from double_check.request_token.handlers import check_token, request_token

ROUTES = [
    RouteDef(
        'POST',
        r'/request_token',
        request_token,
        {'name': 'request_token'}
    ),
    RouteDef(
        'POST',
        r'/check_token',
        check_token,
        {'name': 'check_token'}
    )
]
