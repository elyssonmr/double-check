class BaseExeception(Exception):
    def __init__(
        self,
        message: str = 'Something is not right',
        error_code: str = 'unexpected_error',
        info: dict = None
    ):
        self.message = message
        self.error_code = error_code
        self.info = info

    @property
    def details(self) -> dict:
        error = {
            'message': self.message,
            'error_code': self.error_code
        }

        if self.info:
            error['info'] = self.info

        return error


class APIException(BaseExeception):
    status_code = 500
