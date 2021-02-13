from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from loguru import logger

from app import config
from app.models.base import User
from app.models.suggestion import Suggestion
from app.utils import markups
from app.utils.states import UserStates


async def cmd_start(message: types.Message, user: User, state: FSMContext):
    logger.info("Start")
    await state.finish()

    await UserStates.Input_suggesting_msg.set()
    await message.answer(
        f"""
Привет!
Отправь свою домашку в любом виде. После проверки модераторами она попадёт в специальный канал со всеми домашками: {config.MAIN_CHANNEL_USERNAME}

У тебя не должнен быть скрытый профиль, в противном случае люди просто не смогут тебе написать.
        """
    )


async def input_suggesting_msg(message: types.Message, user: User, state: FSMContext):
    logger.info("Input suggesting message")

    forwarded_msg = await message.forward(config.MODER_CHANNEL_ID)
    await forwarded_msg.reply(
        "Одобрить?",
        reply_markup=markups.approve_suggestion(forwarded_msg.message_id),
        disable_notification=True,
    )

    await Suggestion.create(id=forwarded_msg.message_id, user=user)
    logger.info(
        f"""Inputed suggesting message
URL: {forwarded_msg.url}
            """
    )

    await message.answer(
        """
Принято! Ожидай пока модераторы проверят твоё сообщение, я тебя оповещу когда они одобрят.

А пока можешь отправить ещё одну домашку
            """
    )


def register_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(
        input_suggesting_msg,
        content_types=ContentType.ANY,
        state=UserStates.Input_suggesting_msg,
    )
