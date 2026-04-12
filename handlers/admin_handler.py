from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
import os
import asyncio
import logging
from datetime import datetime
from handlers.reminders import reminder_subscribers

router = Router()
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    from config import ADMIN_ID
    if ADMIN_ID and user_id == int(ADMIN_ID):
        return True
    return False


def get_admin_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📧 Подписчики")],
        [KeyboardButton(text="📢 Рассылка"), KeyboardButton(text="❌ Ошибки")],
        [KeyboardButton(text="📋 Лог"), KeyboardButton(text="💡 Совет всем")],
        [KeyboardButton(text="🙈 Скрыть меню")],
    ], resize_keyboard=True)


# Все админские кнопки
ADMIN_TEXTS = {
    "📊 Статистика", "📧 Подписчики", "📢 Рассылка",
    "❌ Ошибки", "📋 Лог", "💡 Совет всем", "🙈 Скрыть меню",
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
    
    logger.info(f"Админская кнопка: {text} от user_id={user_id}")
    
    # Проверка админа
    if not is_admin(user_id):
        logger.warning(f"Попытка доступа к админке от user_id={user_id}")
        sent = await message.answer("⛔ У вас нет прав администатора.")
        await _autodel(sent, 5)
        return

    logger.info(f"Админская кнопка: {text} от {message.from_user.id}")

    # Удаляем сообщение с кнопкой
    try:
        await message.bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    if text == "📊 Статистика":
        unique = set()
        count = 0
        try:
            with open('bot.log', 'r', encoding='utf-8') as f:
                for line in f:
                    if 'user_id=' in line:
                        parts = line.split('user_id=')
                        if len(parts) > 1:
                            uid = parts[1].split(')')[0].strip()
                            unique.add(uid)
                            count += 1
        except:
            pass
        sent = await message.answer(
            f"📊 **СТАТИСТИКА**\n\n"
            f"👥 Уникальных: {len(unique)}\n"
            f"📝 Сообщений: {count}\n"
            f"📧 Подписчиков: {len(reminder_subscribers)}",
            reply_markup=get_admin_kb()
        )
        await _autodel(sent, 15)

    elif text == "📧 Подписчики":
        if not reminder_subscribers:
            sent = await message.answer("📧 Подписчиков пока нет.", reply_markup=get_admin_kb())
        else:
            subs = "\n".join(f"• `{uid}`" for uid in sorted(reminder_subscribers))
            if len(subs) > 4000:
                subs = subs[:3900] + "\n\n...ещё"
            sent = await message.answer(f"📧 **ПОДПИСЧИКИ** ({len(reminder_subscribers)}):\n\n{subs}", reply_markup=get_admin_kb())
        await _autodel(sent, 20)

    elif text == "📢 Рассылка":
        await message.answer(
            "📢 **Режим рассылки**\n\n"
            "Просто напишите текст — он будет отправлен всем подписчикам.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отменить рассылку")]],
                resize_keyboard=True
            )
        )

    elif text == "❌ Отменить рассылку":
        await message.answer("📢 Рассылка отменена.", reply_markup=get_admin_kb())

    elif text == "💡 Совет всем":
        status = await message.answer("📧 Отправляю совет подписчикам...")
        try:
            from handlers.reminders import _send_weekly_tips
            await _send_weekly_tips(message.bot)
            await status.edit_text(f"✅ Совет отправлен {len(reminder_subscribers)} подписчикам!")
        except Exception as e:
            await status.edit_text(f"❌ Ошибка: {e}")
        await _autodel(status, 10)
        sent = await message.answer("✅ Готово", reply_markup=get_admin_kb())
        await _autodel(sent, 5)

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
                sent = await message.answer(f"❌ **ОШИБКИ** ({len(errors)}):\n\n```\n{txt}\n```", reply_markup=get_admin_kb())
        except:
            sent = await message.answer("📋 Лог не найден.", reply_markup=get_admin_kb())
        await _autodel(sent, 20)

    elif text == "📋 Лог":
        try:
            with open('bot.log', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            last = ''.join(lines[-30:])
            if len(last) > 4000:
                last = last[-4000:]
            sent = await message.answer(f"📋 **ЛОГ (30 строк):**\n\n```\n{last}\n```", reply_markup=get_admin_kb())
        except:
            sent = await message.answer("📋 Лог не найден.", reply_markup=get_admin_kb())
        await _autodel(sent, 20)

    elif text == "🙈 Скрыть меню":
        await message.answer("🙈 Админ-меню скрыто. Чтобы вернуть — /admin", reply_markup=ReplyKeyboardRemove())


# === ОБРАБОТЧИК РАССЫЛКИ (ловит текст после нажатия "Рассылка") ===
@router.message(F.text, ~F.text.startswith('/'))
async def handle_broadcast_text(message: Message):
    """Если админ написал текст после нажатия 'Рассылка'"""
    if not is_admin(message.from_user.id):
        return

    text = message.text.strip()
    if not text:
        return

    if not reminder_subscribers:
        await message.answer("📧 Нет подписчиков.", reply_markup=get_admin_kb())
        return

    sent_count = 0
    fail_count = 0
    status = await message.answer(f"📢 **Рассылка...** 0/{len(reminder_subscribers)}")

    for uid in list(reminder_subscribers):
        try:
            await message.bot.send_message(int(uid), text)
            sent_count += 1
        except Exception as e:
            fail_count += 1
            logger.error(f"Рассылка {uid}: {e}")
        if (sent_count + fail_count) % 10 == 0:
            try:
                await status.edit_text(f"📢 **Рассылка...** {sent_count + fail_count}/{len(reminder_subscribers)}")
            except:
                pass

    await status.edit_text(f"✅ **Готово!**\n📢 Отправлено: {sent_count}\n❌ Ошибок: {fail_count}")
    await asyncio.sleep(5)
    await message.bot.delete_message(message.chat.id, status.message_id)
    await message.answer("✅ Рассылка завершена.", reply_markup=get_admin_kb())


# === Команды ===
@router.message(Command('admin'))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("👤 **Админ-панель** — используйте кнопки внизу.", reply_markup=get_admin_kb())


@router.message(Command('hide_admin'))
async def cmd_hide(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("🙈 Админ-меню скрыто. /admin — вернуть.", reply_markup=ReplyKeyboardRemove())
