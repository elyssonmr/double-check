from aiohttp.web import json_response, middleware, Request, RequestHandler

from double_check.base.exceptions import APIException


@middleware
async def exception_middleware(request: Request, handler: RequestHandler):
    try:
        response = await handler(request)
    except APIException as err:
        return json_response(
            err.details,
            status=err.status_code
        )

    return response
