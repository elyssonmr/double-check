from aiohttp.web import Application

from double_check.backends.ramos import configure_ramos
from double_check.handlers import about_hanlder
from double_check.request_token.routes import ROUTES as token_routes


def create_app():
    configure_ramos()
    app = Application()
    app.router.add_routes(token_routes)

    app.router.add_get(r'/about', about_hanlder, name='about')

    return app
