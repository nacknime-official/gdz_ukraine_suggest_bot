import logging
import sys
import warnings

from aiogram.types.user import User
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup():
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.configure(
        handlers=[
            dict(
                sink=sys.stderr,
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>User {extra[user_id]}: {message}</level>",
                enqueue=True,
            )
        ],
        patcher=lambda record: record["extra"].update(
            user_id=user.id if (user := User.get_current()) else "Unknown"
        ),
    )
