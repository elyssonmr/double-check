from aiohttp.web import Application

from double_check.handlers import about_hanlder


def create_app():
    app = Application()
    app.router.add_get(r'/', about_hanlder)

    return app
