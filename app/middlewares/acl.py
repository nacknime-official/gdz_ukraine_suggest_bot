from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app import config
from app.models.user import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User, message: types.Message):
        user_id = user.id

        user_db: User = (await User.get_or_create(id=user_id))[0]

        if user_db.is_banned:
            await message.answer(
                f"""
Вы были забанены. Все вопросы сюда - {config.GDZ_CHAT_USERNAME}
                    """,
            )
            raise CancelHandler()

        data["user"] = user_db

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message)

    async def on_pre_process_callback_query(
        self, query: types.CallbackQuery, data: dict
    ):
        await self.setup_chat(data, query.from_user, query.message)
