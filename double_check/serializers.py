from marshmallow import fields, Schema


class RequestTokenSerializer(Schema):
    site_name = fields.Str(required=True)
    username = fields.Str(required=True)
    action = fields.Str()
