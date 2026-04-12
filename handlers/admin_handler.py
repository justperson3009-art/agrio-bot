from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os
import asyncio
import logging
from datetime import datetime
from feedback_db import (
    get_stats, get_complaints, delete_complaint,
    get_subscribers_list, add_subscriber, remove_subscriber
)

router = Router()
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    from config import ADMIN_ID
    if ADMIN_ID and user_id == int(ADMIN_ID):
        return True
    return False


def get_admin_kb() -> ReplyKeyboardMarkup:
    """Админ-клавиатура — ВСЕГДА видна админу"""
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📧 Подписчики")],
        [KeyboardButton(text="📢 Рассылка"), KeyboardButton(text="📝 Жалобы")],
        [KeyboardButton(text="❌ Ошибки")],
    ], resize_keyboard=True)


# Все админские кнопки
ADMIN_TEXTS = {
    "📊 Статистика", "📧 Подписчики", "📢 Рассылка",
    "📝 Жалобы", "❌ Ошибки",
    "❌ Отменить рассылку"
}


async def _autodel(msg, seconds=15):
    """Удалить сообщение через N секунд"""
    try:
        await asyncio.sleep(seconds)
        await msg.bot.delete_message(msg.chat.id, msg.message_id)
    except:
        pass


# === ОБРАБОТЧИК ВСЕХ АДМИНСКИХ КНОПОК ===
@router.message(F.text.in_(ADMIN_TEXTS))
async def handle_admin_buttons(message: Message):
    text = message.text
    user_id = message.from_user.id

    logger.info(f"АДМИНСКАЯ КНОПКА: '{text}' от user_id={user_id}")

    # Проверка админа
    if not is_admin(user_id):
        logger.warning(f"Попытка доступа к админке от user_id={user_id}")
        sent = await message.answer("⛔ У вас нет прав администатора.")
        await _autodel(sent, 5)
        return

    # Удаляем сообщение с кнопкой
    try:
        await message.bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    if text == "📊 Статистика":
        stats = get_stats()
        sent = await message.answer(
            f"📊 **СТАТИСТИКА AGRIO BOT**\n\n"
            f"👥 Пользователей: **{stats['total_users']}**\n"
            f"📝 Всего запросов: **{stats['total_requests']}**\n"
            f"📈 Запросов за неделю: **{stats['weekly_requests']}**\n\n"
            f"👍 Полезных ответов: **{stats['positive_feedback']}**\n"
            f"👎 Не полезных ответов: **{stats['negative_feedback']}**\n\n"
            f"📧 Подписчиков на рассылку: **{stats['subscribers']}**\n"
            f"📝 Жалоб с комментариями: **{stats['complaints_count']}**",
            reply_markup=get_admin_kb(),
            parse_mode="Markdown"
        )
        await _autodel(sent, 20)

    elif text == "📧 Подписчики":
        subs = get_subscribers_list()
        if not subs:
            sent = await message.answer("📧 Подписчиков пока нет.", reply_markup=get_admin_kb())
        else:
            lines = []
            for s in subs:
                lines.append(f"• `{s['user_id']}` (с {s['subscribed_at'][:10]})")
            subs_text = "\n".join(lines)
            if len(subs_text) > 4000:
                subs_text = subs_text[:3900] + "\n\n...ещё"
            sent = await message.answer(
                f"📧 **ПОДПИСЧИКИ** ({len(subs)}):\n\n{subs_text}",
                reply_markup=get_admin_kb(),
                parse_mode="Markdown"
            )
        await _autodel(sent, 20)

    elif text == "📢 Рассылка":
        await message.answer(
            "📢 **Режим рассылки**\n\n"
            "Просто напишите текст — он будет отправлен всем подписчикам.\n"
            "Для отмены нажмите **❌ Отменить рассылку**",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отменить рассылку")]],
                resize_keyboard=True
            )
        )
        # Включаем режим рассылки
        import main
        main.broadcast_mode[user_id] = True

    elif text == "❌ Отменить рассылку":
        import main
        main.broadcast_mode.pop(user_id, None)
        sent = await message.answer("📢 Рассылка отменена.", reply_markup=get_admin_kb())
        await _autodel(sent, 5)

    elif text == "📝 Жалобы":
        complaints = get_complaints(limit=15)
        if not complaints:
            sent = await message.answer("✅ Жалоб нет!", reply_markup=get_admin_kb())
        else:
            txt = ""
            for c in complaints:
                txt += (
                    f"👤 ID: `{c['user_id']}`\n"
                    f"📝 Запрос: {c['message_text'][:100]}\n"
                    f"❌ Жалоба: {c['comment'][:200]}\n"
                    f"🕐 {c['created_at']}\n\n"
                )
            if len(txt) > 4000:
                txt = txt[:4000] + "..."
            sent = await message.answer(
                f"📝 **ЖАЛОБЫ** ({len(complaints)}):\n\n{txt}",
                reply_markup=get_admin_kb(),
                parse_mode="Markdown"
            )
        await _autodel(sent, 25)

    elif text == "❌ Ошибки":
        try:
            with open('bot.log', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            errors = [l for l in lines if 'ERROR' in l or 'CRITICAL' in l][-20:]
            if not errors:
                sent = await message.answer("✅ Ошибок нет!", reply_markup=get_admin_kb())
            else:
                txt = ''.join(errors)
                if len(txt) > 4000:
                    txt = txt[-4000:]
                sent = await message.answer(
                    f"❌ **ОШИБКИ** ({len(errors)}):\n\n```\n{txt}\n```",
                    reply_markup=get_admin_kb()
                )
        except:
            sent = await message.answer("📋 Лог не найден.", reply_markup=get_admin_kb())
        await _autodel(sent, 20)


# === Команды ===
@router.message(Command('admin'))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("👤 **Админ-панель** — используйте кнопки внизу.", reply_markup=get_admin_kb())
