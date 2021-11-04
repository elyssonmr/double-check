import uvloop

from double_check.application import create_app


def main(argv):
    uvloop.install()
    print('Starting server')
    return create_app()
