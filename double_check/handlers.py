import json

from aiohttp.web import Request, Response


async def about_hanlder(request: Request):
    return Response(text=json.dumps({'Name': 'Double Check'}))
