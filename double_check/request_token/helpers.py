from double_check.request_token.serializers import RequestTokenSerializer


def validate_request_token_data(request_body: dict) -> dict:
    return RequestTokenSerializer().load(request_body)
