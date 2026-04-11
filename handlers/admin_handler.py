from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import os
import logging
from datetime import datetime
from handlers.reminders import reminder_subscribers

router = Router()
ADMIN_IDS = set()

def is_admin(user_id: int) -> bool:
    from config import ADMIN_ID
    if ADMIN_ID and user_id == int(ADMIN_ID):
        return True
    return user_id in ADMIN_IDS

def add_admin(user_id: int):
    ADMIN_IDS.add(user_id)

@router.message(Command('admin'))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет прав администратора.")
        return
    add_admin(message.from_user.id)
    await message.answer(
        "👤 **АДМИН-ПАНЕЛЬ**\n\n"
        "📊 `/users` — статистика\n"
        "📧 `/subscribers` — подписчики\n"
        "📢 `/broadcast [текст]` — рассылка\n"
        "📋 `/logs [N]` — последние N строк лога\n"
        "❌ `/errors` — последние ошибки\n"
        "💡 `/send_tip` — отправить совет всем"
    )

@router.message(Command('users'))
async def cmd_users(message: Message):
    if not is_admin(message.from_user.id):
        return
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
    await message.answer(
        f"📊 **СТАТИСТИКА**\n\n"
        f"👥 Уникальных: {len(unique_users)}\n"
        f"📝 Сообщений: {user_messages}\n"
        f"📧 Подписчиков: {len(reminder_subscribers)}"
    )

@router.message(Command('subscribers'))
async def cmd_subscribers(message: Message):
    if not is_admin(message.from_user.id):
        return
    if not reminder_subscribers:
        await message.answer("📧 Подписчиков пока нет.")
        return
    subs = "\n".join(f"• `{uid}`" for uid in sorted(reminder_subscribers))
    await message.answer(f"📧 **ПОДПИСЧИКИ** ({len(reminder_subscribers)}):\n\n{subs}")

@router.message(Command('broadcast'))
async def cmd_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return
    text = message.text.replace('/broadcast', '').strip()
    if not text:
        await message.answer("📢 **Использование:**\n`/broadcast [текст]`")
        return
    if not reminder_subscribers:
        await message.answer("📧 Нет подписчиков.")
        return
    sent = 0
    failed = 0
    status_msg = await message.answer(f"📢 **Рассылка...** 0/{len(reminder_subscribers)}")
    for user_id in list(reminder_subscribers):
        try:
            await message.bot.send_message(user_id, text)
            sent += 1
        except Exception as e:
            failed += 1
            logging.error(f"Ошибка рассылки {user_id}: {e}")
        if (sent + failed) % 10 == 0:
            try:
                await status_msg.edit_text(f"📢 **Рассылка...** {sent + failed}/{len(reminder_subscribers)}")
            except:
                pass
    await status_msg.edit_text(f"✅ **Готово!**\n📢 Отправлено: {sent}\n❌ Ошибок: {failed}")

@router.message(Command('logs'))
async def cmd_logs(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    n = 20
    if len(parts) > 1:
        try:
            n = min(int(parts[1]), 100)
        except:
            pass
    log_file = 'bot.log'
    if not os.path.exists(log_file):
        await message.answer("📋 Лог не найден.")
        return
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    last = ''.join(lines[-n:])
    if len(last) > 4000:
        last = last[-4000:]
    await message.answer(f"📋 **ЛОГ (последние {n} строк):**\n\n```\n{last}\n```")

@router.message(Command('errors'))
async def cmd_errors(message: Message):
    if not is_admin(message.from_user.id):
        return
    log_file = 'bot.log'
    if not os.path.exists(log_file):
        await message.answer("📋 Лог не найден.")
        return
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    errors = [l for l in lines if 'ERROR' in l or 'CRITICAL' in l][-20:]
    if not errors:
        await message.answer("✅ Ошибок нет!")
        return
    text = ''.join(errors)
    if len(text) > 4000:
        text = text[-4000:]
    await message.answer(f"❌ **ОШИБКИ** ({len(errors)}):\n\n```\n{text}\n```")

@router.message(Command('send_tip'))
async def cmd_send_tip(message: Message):
    if not is_admin(message.from_user.id):
        return
    from handlers.reminders import _send_weekly_tips
    await message.answer("📧 Отправляю совет...")
    await _send_weekly_tips(message.bot)
    await message.answer(f"✅ Совет отправлен {len(reminder_subscribers)} подписчикам!")
