from tortoise import fields

from app import config
from app.models.db import TimedBaseModel


class User(TimedBaseModel):
    id = fields.IntField(pk=True)
    warns = fields.IntField(default=0)

    suggestions: fields.ReverseRelation["models.Suggestion"]

    class Meta:
        table = "users"

    @property
    def is_banned(self):
        return self.warns == config.WARNS_COUNT_TO_BE_BANNED
