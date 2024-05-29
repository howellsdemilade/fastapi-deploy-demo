from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)

class TokenTable(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='tokens')
    access_token = fields.CharField(max_length=255)
    refresh_token = fields.CharField(max_length=255)
    status = fields.BooleanField(default=True)
    created_date = fields.DatetimeField(auto_now_add=True)