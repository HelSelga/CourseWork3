from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str()
    surname = fields.Str()
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    favorite_genre = fields.Str()
