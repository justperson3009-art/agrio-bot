"""
Обработчик команды /catalog и текстовых запросов о каталоге
"""

import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from responses.catalog_responses import (
    get_catalog_response,
    get_catalog_inline,
    is_catalog_command,
    is_catalog_question
)

logger = logging.getLogger(__name__)
router = Router(name="catalog")


@router.message(Command("catalog"))
async def cmd_catalog(message: Message):
    """Обработчик команды /catalog"""
    logger.info(f"Пользователь {message.from_user.id} отправил /catalog")
    await message.answer(get_catalog_response())


@router.message(F.text.lower().regexp(r'^(каталог|коталог)(\s*семян)?$'))
async def cmd_catalog_text(message: Message):
    """Обработчик команды 'Каталог' текстом (в т.ч. с опечаткой 'Коталог')"""
    logger.info(f"Пользователь {message.from_user.id} написал 'Каталог' текстом")
    await message.answer(get_catalog_response())


def check_catalog_commands(user_text: str) -> bool:
    """
    Проверка: является ли сообщение командой каталога.
    Возвращает True если нужно отправить каталог.
    """
    # Проверка: команда "Каталог" (в т.ч. с опечаткой "Коталог")
    if is_catalog_command(user_text):
        logger.info("Команда 'Каталог' — отправляем полный каталог")
        return True

    # Проверка: вопрос про ассортимент семян?
    if is_catalog_question(user_text):
        logger.info("Вопрос про ассортимент — отправляем готовый каталог")
        return True

    return False
