import pytest

from double_check.backends.ramos import configure_ramos


@pytest.fixture(autouse=True)
def config_ramos():
    configure_ramos()
