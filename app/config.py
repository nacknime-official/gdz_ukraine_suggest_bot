import os
from pathlib import Path

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MODER_CHANNEL_ID = str(os.getenv("MODER_CHANNEL_ID"))
MAIN_CHANNEL_ID = str(os.getenv("MAIN_CHANNEL_ID"))
GDZ_CHAT_USERNAME = str(os.getenv("GDZ_CHAT_USERNAME"))
MAIN_CHANNEL_USERNAME = str(os.getenv("MAIN_CHANNEL_USERNAME"))

WARNS_COUNT_TO_BE_BANNED = 3


POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", default=5432)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="")
POSTGRES_USER = os.getenv("POSTGRES_USER", default="aiogram")
POSTGRES_DB = os.getenv("POSTGRES_DB", default="aiogram")
POSTGRES_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_HOST = os.getenv("REDIS_HOST", default="localhost")
REDIS_PORT = os.getenv("REDIS_PORT", default=6379)
REDIS_FSM_DB = int(str(os.getenv("REDIS_FSM_DB", default=0)))
REDIS_FSM_PREFIX = os.getenv("REDIS_FSM_PREFIX", default="fsm")

TORTOISE_ORM = {
    "connections": {"default": POSTGRES_URI},
    "apps": {
        "models": {
            "models": ["app.models.base", "aerich.models"],
            "default_connection": "default",
        },
    },
}
