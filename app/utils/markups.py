from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData

suggestion_cb = CallbackData("sugg", "choice", "suggestion_id")

BTN_SUGGESTION_APPROVE = "✅Одобрить"
BTN_SUGGESTION_GIVE_WARN = "⚠️Выдать предупреждение"

CB_SUGGESTION_APPROVE = "approve"
CB_SUGGESTION_GIVE_WARN = "warn"


def approve_suggestion(suggestion_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            BTN_SUGGESTION_APPROVE,
            callback_data=suggestion_cb.new(
                choice=CB_SUGGESTION_APPROVE, suggestion_id=suggestion_id
            ),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            BTN_SUGGESTION_GIVE_WARN,
            callback_data=suggestion_cb.new(
                choice=CB_SUGGESTION_GIVE_WARN, suggestion_id=suggestion_id
            ),
        )
    )
    return markup
