from marshmallow import fields, Schema


class RequestTokenSerializer(Schema):
    site_name = fields.Str(required=True)
    username = fields.Str(required=True)
    action = fields.Str(load_default='Login')


class CheckTokenSerializer(Schema):
    request_token = fields.Str(required=True)
    user_token = fields.Str(required=True)
