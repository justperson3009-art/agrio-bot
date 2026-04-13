"""
Обработчик пользовательских сообщений (гибридная система ИИ)
"""

import logging
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from hybrid_ai import HybridAgroConsultant
from moderation import moderate_message
from logger import log_ai_request
from responses.catalog_responses import get_catalog_response
from handlers.catalog_handler import check_catalog_commands
from responses.command_responses import (
    get_moderation_block_response,
    get_injection_block_response,
    get_mention_only_prompt
)

logger = logging.getLogger(__name__)


# Хранилище контекста диалога для каждого пользователя
user_dialogs = {}


def get_user_context(user_id: int) -> list:
    """Получить контекст диалога пользователя"""
    return user_dialogs.get(user_id, [])[-5:]  # Последние 5 сообщений


def add_to_context(user_id: int, role: str, content: str):
    """Добавить сообщение в контекст диалога пользователя"""
    if user_id not in user_dialogs:
        user_dialogs[user_id] = []
    user_dialogs[user_id].append({"role": role, "content": content})
    # Ограничиваем размер контекста
    if len(user_dialogs[user_id]) > 5:
        user_dialogs[user_id] = user_dialogs[user_id][-5:]


async def handle_user_message(
    message: Message,
    state: FSMContext,
    hybrid_consultant: HybridAgroConsultant,
    yandex_service,
    bot_info_cache: dict,
    chat_mode: str,
    is_group: bool
):
    """Обработка сообщений от пользователя (гибридная система)"""
    user_text = message.text
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"
    chat_id = message.chat.id

    logger.info(f"=== ВХОДЯЩЕЕ СООБЩЕНИЕ ===")
    logger.info(f"От: {username} (user_id={user_id})")
    logger.info(f"Чат: {chat_id}, тип: {message.chat.type}")
    logger.info(f"Текст: {user_text[:100]}")

    # Если группа или mention_only — проверяем упоминание бота
    if is_group or chat_mode == "mention":
        mentioned = _is_bot_mentioned(message, bot_info_cache)
        logger.info(f"Бот упомянут: {mentioned}")

        if not mentioned:
            logger.info(f"Бот не упомянут — игнорируем")
            return

        # Удаляем упоминание бота из текста
        bot_username = f"@{bot_info_cache.get('username')}"
        user_text = user_text.replace(bot_username, "").strip()
        user_text = user_text.replace(bot_username.lower(), "").strip()

        if not user_text or user_text == "?":
            await message.answer(get_mention_only_prompt(bot_info_cache.get('username', '')))
            return

    # Проверка модерации
    logger.info(f"Проверка модерации для: {user_text[:50]}")
    is_allowed, reason = moderate_message(user_text)
    if not is_allowed:
        logger.warning(f"Модерация заблокировала сообщение от {username}: {reason}")
        await message.answer(get_moderation_block_response())
        return

    logger.info(f"Модерация пройдена")

    # Проверка: команда "Каталог" или вопрос про ассортимент
    if check_catalog_commands(user_text):
        from config import ADMIN_ID
        if user_id == int(ADMIN_ID or 0):
            from handlers.admin_handler import get_admin_kb
            await message.answer(get_catalog_response(), reply_markup=get_admin_kb())
        else:
            from keyboards.feedback_keyboard import get_feedback_keyboard
            await message.answer(get_catalog_response(), reply_markup=get_feedback_keyboard())
        return

    # Проверка на prompt injection
    if _check_injection_attempt(user_text):
        logger.warning(f"Попытка injection от {username}")
        await message.answer(get_injection_block_response())
        return

    logger.info(f"Проверка на injection пройдена")

    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Получаем контекст диалога
    context = get_user_context(user_id)

    # === ГИБРИДНАЯ СИСТЕМА ===
    logger.info("Обработка гибридной системой...")

    try:
        response, source = await hybrid_consultant.get_response(
            message=user_text,
            ai_service=yandex_service,
            dialog_context=context
        )

        logger.info(f"Ответ получен из источника: {source}")

    except Exception as e:
        logger.error(f"Ошибка гибридной системы: {e}")
        response = "Извините, произошла ошибка. Попробуйте позже."
        source = "error"

    # Добавляем в контекст только если ответ от ИИ
    if source == 'ai':
        add_to_context(user_id, "user", user_text)
        add_to_context(user_id, "assistant", response)

    # Логирование
    log_ai_request(user_id, username, user_text, response)

    # Логирование запроса в статистику
    from feedback_db import log_request
    log_request(user_id)

    # Отправка ответа
    from config import ADMIN_ID
    if user_id == int(ADMIN_ID or 0):
        # Админ — всегда ReplyKeyboard с кнопками внизу
        from handlers.admin_handler import get_admin_kb
        await message.answer(response, reply_markup=get_admin_kb())
    else:
        # Обычный пользователь — inline кнопки Полезно/Не полезно
        from keyboards.feedback_keyboard import get_feedback_keyboard
        await message.answer(response, reply_markup=get_feedback_keyboard())

    logger.info(f"Ответ отправлен пользователю (источник: {source})")


def _is_bot_mentioned(message: Message, bot_info_cache: dict) -> bool:
    """Проверить, упомянут ли бот в сообщении"""
    bot_username = bot_info_cache.get("username")
    if not bot_username:
        return False

    # Проверяем упоминание бота по username в тексте
    if f"@{bot_username}" in message.text.lower():
        return True
    # Также проверяем без @
    if bot_username.lower() in message.text.lower():
        return True

    # Проверяем entities для точного упоминания
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mention_text = message.text[entity.offset:entity.offset + entity.length]
                if mention_text.lower() == f"@{bot_username}".lower():
                    return True
            elif entity.type == "text_mention":
                if entity.user and entity.user.id == bot_info_cache.get("id"):
                    return True

    return False


def _check_injection_attempt(message: str) -> bool:
    """Проверка на Prompt Injection"""
    import re
    injection_patterns = [
        r"забудь\s+(все\s+)?инструкци",
        r"игнорируй\s+(инструкци|правила)",
        r"повтори\s+(системн|инструкци)",
        r"раскрой\s+(промпт|настройк)",
        r"ты\s+теперь\s+",
        r"смени\s+роль",
        r"новый\s+приказ",
        r"системное\s+сообщение"
    ]

    message_lower = message.lower()
    for pattern in injection_patterns:
        if re.search(pattern, message_lower):
            logger.warning(f"Попытка prompt injection: {message[:100]}")
            return True
    return False
