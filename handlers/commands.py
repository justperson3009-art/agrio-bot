"""
Обработчики основных команд: /start, /help, /about, /status
"""

import logging
from aiogram import Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import Router

from responses.command_responses import (
    get_start_response,
    get_help_response,
    get_about_response,
    get_status_response,
    get_subscribe_prompt
)

logger = logging.getLogger(__name__)
router = Router(name="commands")


def _get_admin_kb_if_admin(user_id: int):
    """Вернуть админ-клавиатуру только для ADMIN_ID"""
    try:
        from handlers.admin_handler import is_admin, get_admin_kb
        if is_admin(user_id):
            return get_admin_kb()
    except:
        pass
    return None


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    logger.info(f"Пользователь {message.from_user.id} отправил /start")
    kb = _get_admin_kb_if_admin(message.from_user.id)
    if kb:
        await message.answer(get_start_response(), reply_markup=kb)
    else:
        await message.answer(get_start_response())
        # Предложение подписки для новых пользователей
        await message.answer(get_subscribe_prompt())


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    logger.info(f"Пользователь {message.from_user.id} отправил /help")
    await message.answer(get_help_response())


@router.message(Command("about"))
async def cmd_about(message: Message):
    """Обработчик команды /about"""
    logger.info(f"Пользователь {message.from_user.id} отправил /about")
    await message.answer(get_about_response())


@router.message(Command("status"))
async def cmd_status(message: Message):
    """Обработчик команды /status - проверка состояния бота"""
    bot = message.bot
    bot_info = await bot.get_me()

    bot_info_dict = {
        'first_name': bot_info.first_name,
        'username': bot_info.username,
        'id': bot_info.id,
        'can_join_groups': bot_info.can_join_groups,
        'can_read_all_group_messages': bot_info.can_read_all_group_messages
    }

    logger.info(f"Пользователь {message.from_user.id} отправил /status")
    await message.answer(get_status_response(bot_info_dict))
