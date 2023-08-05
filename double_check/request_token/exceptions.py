from double_check.base.exceptions import APIException


class InvalidDataException(APIException):
    status_code = 400


class InvalidJsonException(APIException):
    status_code = 400
