from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subscribe_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура: Подписаться / Не сейчас"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Подписаться бесплатно", callback_data="subscribe:yes"),
    )
    builder.row(
        InlineKeyboardButton(text="❌ Не сейчас", callback_data="subscribe:no"),
    )
    return builder.as_markup()
