from aiohttp.web import Application

from double_check.backends.ramos import configure_ramos
from double_check.base.middlewares import exception_middleware
from double_check.handlers import about_hanlder
from double_check.request_token.routes import ROUTES as token_routes

MIDDLEWARES = [exception_middleware]


def create_app():
    configure_ramos()
    app = Application(middlewares=MIDDLEWARES)
    app.router.add_routes(token_routes)

    app.router.add_get(r'/about', about_hanlder, name='about')

    return app
