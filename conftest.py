from asyncio.futures import Future

import pytest

from double_check.backends.ramos import configure_ramos


@pytest.fixture(autouse=True)
def config_ramos():
    configure_ramos()


@pytest.fixture
def setup_future():
    def setup(result=None):
        future = Future()
        future.set_result(result)
        return future

    return setup
