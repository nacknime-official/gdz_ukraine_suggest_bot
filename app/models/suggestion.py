from tortoise import fields

from app.models.db import TimedBaseModel
from app.models.user import User


class Suggestion(TimedBaseModel):
    id = fields.IntField(pk=True, description="uses message id from moder channel")

    is_approved = fields.BooleanField(default=False)
    is_warned = fields.BooleanField(default=False)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="suggestions"
    )

    class Meta:
        table = "suggestions"
