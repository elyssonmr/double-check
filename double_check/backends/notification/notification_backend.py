class NotificationBackend:
    async def send_token_to_customer(
        self,
        action: str,
        chat_id: str,
        username: str,
        token: str
    ):
        raise NotImplementedError()
