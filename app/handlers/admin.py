from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loguru import logger

from app import config
from app.models.base import User
from app.models.suggestion import Suggestion
from app.utils import markups
from app.utils.markups import suggestion_cb
from app.utils.states import UserStates


async def approve_suggestion(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    user: User,
    state: FSMContext,
):
    await query.answer()
    await query.message.delete_reply_markup()

    choice = callback_data["choice"]
    suggestion_id = callback_data["suggestion_id"]

    suggestion = await Suggestion.get(id=suggestion_id)
    suggestion_user = await suggestion.user

    if choice == markups.CB_SUGGESTION_APPROVE:
        logger.info(
            f"Approving suggestion \
https://t.me/c/{config.MODER_CHANNEL_ID[4:]}/{suggestion_id}..."
        )

        forwarded_msg = await query.bot.forward_message(
            config.MAIN_CHANNEL_ID, config.MODER_CHANNEL_ID, suggestion_id
        )

        suggestion.is_approved = True
        await suggestion.save()

        await query.bot.send_message(
            suggestion_user.id,
            f"Ваша домашка была одобрена и опубликована, вот ссылка: {forwarded_msg.url}",
        )

        await query.message.edit_text("✅Одобрено")

        logger.info(
            f"Suggestion \
https://t.me/c/{config.MODER_CHANNEL_ID[4:]}/{suggestion_id} \
has been approved in main channel: \
{forwarded_msg.url}"
        )

    elif choice == markups.CB_SUGGESTION_GIVE_WARN:
        logger.info(
            f"Giving warn to the author \
{suggestion_user.id} of suggestion \
https://t.me/c/{config.MODER_CHANNEL_ID[4:]}/{suggestion_id}..."
        )

        suggestion.is_warned = True
        suggestion_user.warns += 1
        await suggestion.save()
        await suggestion_user.save()

        await query.bot.send_message(
            suggestion_user.id,
            f"""
Модераторы выдали предупреждение за вашу домашку.
{suggestion_user.warns}/{config.WARNS_COUNT_TO_BE_BANNED} предупреждений до бана.
Будьте внимательнее в следующие разы :)
            """,
        )

        await query.message.edit_text("⚠️Выдано предупреждение")

        logger.info(
            f"Author {suggestion_user.id} of suggestion \
https://t.me/c/{config.MODER_CHANNEL_ID[4:]}/{suggestion_id} \
has been warned. \
{suggestion_user.warns}/{config.WARNS_COUNT_TO_BE_BANNED}"
        )


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        approve_suggestion, suggestion_cb.filter(), state="*"
    )
