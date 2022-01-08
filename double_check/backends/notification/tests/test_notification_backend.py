import pytest

from double_check.backends.notification import NotificationBackend


@pytest.fixture
def base_backend():
    return NotificationBackend()


async def test_send_token_to_customer_should_not_implemented(base_backend):
    with pytest.raises(NotImplementedError) as err:
        await base_backend.send_token_to_customer(
            'chat_id',
            'username',
            'token'
        )

    assert isinstance(err.value, NotImplementedError)
