"""
Inline-клавиатура для обратной связи (Полезно / Не полезно)
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_feedback_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопками Полезно/Не полезно"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👍 Полезно", callback_data="feedback:positive"),
        InlineKeyboardButton(text="👎 Не полезно", callback_data="feedback:negative"),
    )
    return builder.as_markup()
