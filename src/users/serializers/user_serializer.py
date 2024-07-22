from marshmallow import Schema, fields
from marshmallow_validators.wtforms import from_wtforms
from wtforms.validators import Email, Length

from settings import settings


class CreateUserRequestSerializer(Schema):
    email = fields.Str(required=True, validate=from_wtforms([Email()], locales=settings.locales))
    username = fields.Str(
        required=True,
        validate=from_wtforms([Length(min=3, max=120)], locales=settings.locales)
    )
    password = fields.Str(
        required=True,
        validate=from_wtforms([Length(min=8, max=300)], locales=settings.locales)
    )


class CreateUserResponseSerializer(Schema):
    id = fields.Str(required=True)
    email = fields.Str(required=True)
    username = fields.Str(required=True)
