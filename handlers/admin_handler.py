from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import os
import logging
from datetime import datetime
from handlers.reminders import reminder_subscribers
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()
logger = logging.getLogger(__name__)


class AdminStates(StatesGroup):
    waiting_for_broadcast = State()


def is_admin(user_id: int) -> bool:
    """Только создатель бота (ADMIN_ID из .env)"""
    from config import ADMIN_ID
    if ADMIN_ID and user_id == int(ADMIN_ID):
        return True
    return False


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Админ-кнопки внизу экрана (ReplyKeyboard)"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="📧 Подписчики"),
            ],
            [
                KeyboardButton(text="📢 Рассылка"),
                KeyboardButton(text="❌ Ошибки"),
            ],
            [
                KeyboardButton(text="📋 Лог"),
                KeyboardButton(text="💡 Совет всем"),
            ],
            [
                KeyboardButton(text="🙈 Скрыть меню"),
            ],
        ],
        resize_keyboard=True
    )


async def _delete_msg(bot, chat_id: int, msg_id: int):
    """Безопасное удаление сообщения"""
    try:
        await bot.delete_message(chat_id, msg_id)
    except:
        pass


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    """Показать админ-кнопки"""
    if not is_admin(message.from_user.id):
        return
    await message.answer("👤 **Админ-панель активна**", reply_markup=get_admin_keyboard())


@router.message(Command('hide_admin'))
async def cmd_hide_admin(message: Message):
    """Скрыть админ-кнопки"""
    from aiogram.types import ReplyKeyboardRemove
    await message.answer("🙈 Админ-меню скрыто", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "🙈 Скрыть меню")
async def hide_menu(message: Message):
    if not is_admin(message.from_user.id):
        return
    from aiogram.types import ReplyKeyboardRemove
    await _delete_msg(message.bot, message.chat.id, message.message_id)
    await message.answer("🙈 Админ-меню скрыто. Чтобы вернуть — /admin", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "📊 Статистика")
async def btn_stats(message: Message):
    if not is_admin(message.from_user.id):
        return

    # Удаляем сообщение пользователя
    await _delete_msg(message.bot, message.chat.id, message.message_id)

    unique_users = set()
    user_messages = 0
    log_file = 'bot.log'
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'user_id=' in line:
                    parts = line.split('user_id=')
                    if len(parts) > 1:
                        uid = parts[1].split(')')[0].strip()
                        unique_users.add(uid)
                        user_messages += 1

    stats_text = (
        f"📊 **СТАТИСТИКА**\n\n"
        f"👥 Уникальных: {len(unique_users)}\n"
        f"📝 Сообщений: {user_messages}\n"
        f"📧 Подписчиков: {len(reminder_subscribers)}"
    )

    sent = await message.answer(stats_text, reply_markup=get_admin_keyboard())

    # Автоудаление через 15 секунд
    import asyncio
    await asyncio.sleep(15)
    await _delete_msg(message.bot, message.chat.id, sent.message_id)


@router.message(F.text == "📧 Подписчики")
async def btn_subs(message: Message):
    if not is_admin(message.from_user.id):
        return

    await _delete_msg(message.bot, message.chat.id, message.message_id)

    if not reminder_subscribers:
        sent = await message.answer("📧 Подписчиков пока нет.", reply_markup=get_admin_keyboard())
    else:
        subs = "\n".join(f"• `{uid}`" for uid in sorted(reminder_subscribers))
        text = f"📧 **ПОДПИСЧИКИ** ({len(reminder_subscribers)}):\n\n{subs}"
        # Ограничиваем длину
        if len(text) > 4000:
            text = text[:3900] + "\n\n... (ещё)"
        sent = await message.answer(text, reply_markup=get_admin_keyboard())

    import asyncio
    await asyncio.sleep(20)
    await _delete_msg(message.bot, message.chat.id, sent.message_id)


@router.message(F.text == "📢 Рассылка")
async def btn_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return

    await _delete_msg(message.bot, message.chat.id, message.message_id)

    sent = await message.answer(
        "📢 **Режим рассылки**\n\n"
        "Просто напишите текст — он будет отправлен всем подписчикам.\n\n"
        "Или нажмите «Отменить» для выхода.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❌ Отменить рассылку")]],
            resize_keyboard=True
        )
    )

    import asyncio
    await asyncio.sleep(30)
    await _delete_msg(message.bot, message.chat.id, sent.message_id)


@router.message(F.text == "❌ Отменить рассылку")
async def cancel_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return
    await _delete_msg(message.bot, message.chat.id, message.message_id)
    await message.answer("📢 Рассылка отменена.", reply_markup=get_admin_keyboard())


@router.message(F.text == "💡 Совет всем")
async def btn_send_tip(message: Message):
    if not is_admin(message.from_user.id):
        return

    await _delete_msg(message.bot, message.chat.id, message.message_id)

    from handlers.reminders import _send_weekly_tips
    status = await message.answer("📧 Отправляю совет подписчикам...")

    try:
        await _send_weekly_tips(message.bot)
        await status.edit_text(f"✅ Совет отправлен {len(reminder_subscribers)} подписчикам!")
    except Exception as e:
        await status.edit_text(f"❌ Ошибка: {e}")

    import asyncio
    await asyncio.sleep(10)
    await _delete_msg(message.bot, message.chat.id, status.message_id)
    sent = await message.answer("✅ Готово", reply_markup=get_admin_keyboard())
    await asyncio.sleep(5)
    await _delete_msg(message.bot, message.chat.id, sent.message_id)


@router.message(F.text == "❌ Ошибки")
async def btn_errors(message: Message):
    if not is_admin(message.from_user.id):
        return

    await _delete_msg(message.bot, message.chat.id, message.message_id)

    log_file = 'bot.log'
    if not os.path.exists(log_file):
        sent = await message.answer("📋 Лог не найден.", reply_markup=get_admin_keyboard())
    else:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        errors = [l for l in lines if 'ERROR' in l or 'CRITICAL' in l][-20:]
        if not errors:
            sent = await message.answer("✅ Ошибок нет!", reply_markup=get_admin_keyboard())
        else:
            text = ''.join(errors)
            if len(text) > 4000:
                text = text[-4000:]
            sent = await message.answer(f"❌ **ОШИБКИ** ({len(errors)}):\n\n```\n{text}\n```", reply_markup=get_admin_keyboard())

    import asyncio
    await asyncio.sleep(20)
    await _delete_msg(message.bot, message.chat.id, sent.message_id)


@router.message(F.text == "📋 Лог")
async def btn_logs(message: Message):
    if not is_admin(message.from_user.id):
        return

    await _delete_msg(message.bot, message.chat.id, message.message_id)

    log_file = 'bot.log'
    if not os.path.exists(log_file):
        sent = await message.answer("📋 Лог не найден.", reply_markup=get_admin_keyboard())
    else:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        last = ''.join(lines[-30:])
        if len(last) > 4000:
            last = last[-4000:]
        sent = await message.answer(f"📋 **ЛОГ (30 строк):**\n\n```\n{last}\n```", reply_markup=get_admin_keyboard())

    import asyncio
    await asyncio.sleep(20)
    await _delete_msg(message.bot, message.chat.id, sent.message_id)
