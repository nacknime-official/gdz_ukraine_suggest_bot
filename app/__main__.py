import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger
from tortoise import Tortoise

from app import config
from app.handlers.admin import register_admin
from app.handlers.base import register_base
from app.middlewares.acl import ACLMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.utils import logging


async def main():
    # logging
    logging.setup()

    ### aiogram
    bot = Bot(config.TELEGRAM_TOKEN)
    storage = RedisStorage2(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_FSM_DB,
        prefix=config.REDIS_FSM_PREFIX,
    )
    dp = Dispatcher(bot, storage=storage)

    # middlewares
    dp.middleware.setup(ThrottlingMiddleware(limit=0.7))
    dp.middleware.setup(ACLMiddleware())

    # handlers
    register_base(dp)
    register_admin(dp)

    # start
    await Tortoise.init(config=config.TORTOISE_ORM)

    try:
        await dp.start_polling()
    finally:
        await Tortoise.close_connections()

        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
