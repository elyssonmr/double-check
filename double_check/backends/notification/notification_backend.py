class NotificationBackend:
    async def send_token_to_customer(
        self,
        chat_id: str,
        username: str,
        token: str
    ):
        raise NotImplementedError()
