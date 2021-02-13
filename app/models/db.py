from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    class Meta:
        abstract = True


class TimedBaseModel(BaseModel):
    class Meta:
        abstract = True

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
