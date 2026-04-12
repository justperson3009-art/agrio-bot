from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os
import logging
from datetime import datetime
from handlers.reminders import reminder_subscribers

router = Router()
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    """Только создатель бота (ADMIN_ID из .env)"""
    from config import ADMIN_ID
    if ADMIN_ID and user_id == int(ADMIN_ID):
        return True
    return False


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Админ-кнопка (только для ADMIN_ID)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin:users"),
            InlineKeyboardButton(text="📧 Подписчики", callback_data="admin:subs"),
        ],
        [
            InlineKeyboardButton(text="📢 Рассылка", callback_data="admin:broadcast"),
            InlineKeyboardButton(text="❌ Ошибки", callback_data="admin:errors"),
        ],
        [
            InlineKeyboardButton(text="📋 Лог", callback_data="admin:logs"),
            InlineKeyboardButton(text="💡 Отправить совет", callback_data="admin:send_tip"),
        ],
    ])


@router.callback_query(lambda c: c.data and c.data.startswith('admin:'))
async def admin_callback(callback):
    """Обработка админских кнопок"""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет прав", show_alert=True)
        return

    action = callback.data.split(':', 1)[1]

    if action == 'users':
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
        await callback.message.answer(
            f"📊 **СТАТИСТИКА**\n\n"
            f"👥 Уникальных: {len(unique_users)}\n"
            f"📝 Сообщений: {user_messages}\n"
            f"📧 Подписчиков: {len(reminder_subscribers)}",
            reply_markup=get_admin_keyboard()
        )

    elif action == 'subs':
        if not reminder_subscribers:
            await callback.message.answer("📧 Подписчиков пока нет.", reply_markup=get_admin_keyboard())
        else:
            subs = "\n".join(f"• `{uid}`" for uid in sorted(reminder_subscribers))
            await callback.message.answer(f"📧 **ПОДПИСЧИКИ** ({len(reminder_subscribers)}):\n\n{subs}", reply_markup=get_admin_keyboard())

    elif action == 'errors':
        log_file = 'bot.log'
        if not os.path.exists(log_file):
            await callback.message.answer("📋 Лог не найден.", reply_markup=get_admin_keyboard())
            return
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        errors = [l for l in lines if 'ERROR' in l or 'CRITICAL' in l][-20:]
        if not errors:
            await callback.message.answer("✅ Ошибок нет!", reply_markup=get_admin_keyboard())
        else:
            text = ''.join(errors)
            if len(text) > 4000:
                text = text[-4000:]
            await callback.message.answer(f"❌ **ОШИБКИ** ({len(errors)}):\n\n```\n{text}\n```", reply_markup=get_admin_keyboard())

    elif action == 'logs':
        log_file = 'bot.log'
        if not os.path.exists(log_file):
            await callback.message.answer("📋 Лог не найден.", reply_markup=get_admin_keyboard())
            return
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        last = ''.join(lines[-30:])
        if len(last) > 4000:
            last = last[-4000:]
        await callback.message.answer(f"📋 **ЛОГ (30 строк):**\n\n```\n{last}\n```", reply_markup=get_admin_keyboard())

    elif action == 'send_tip':
        from handlers.reminders import _send_weekly_tips
        await callback.message.answer("📧 Отправляю совет...")
        await _send_weekly_tips(callback.message.bot)
        await callback.message.answer(f"✅ Совет отправлен {len(reminder_subscribers)} подписчикам!", reply_markup=get_admin_keyboard())

    elif action == 'broadcast':
        await callback.message.answer(
            "📢 **Рассылка**\n\n"
            "Напишите текст для рассылки, затем нажмите кнопку «Отправить».\n\n"
            "Или используйте команду: `/broadcast [текст]`",
            reply_markup=get_admin_keyboard()
        )

    await callback.answer()


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    """Показать админ-кнопки"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет прав администратора.")
        return
    await message.answer(
        "👤 **АДМИН-ПАНЕЛЬ**\n\n"
        "Используйте кнопки ниже или команды:\n"
        "• `/users` — статистика\n"
        "• `/subscribers` — подписчики\n"
        "• `/broadcast [текст]` — рассылка\n"
        "• `/logs [N]` — лог\n"
        "• `/errors` — ошибки\n"
        "• `/send_tip` — совет всем",
        reply_markup=get_admin_keyboard()
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
    kb = get_admin_keyboard() if is_admin(message.from_user.id) else None
    await message.answer(
        f"📊 **СТАТИСТИКА**\n\n"
        f"👥 Уникальных: {len(unique_users)}\n"
        f"📝 Сообщений: {user_messages}\n"
        f"📧 Подписчиков: {len(reminder_subscribers)}",
        reply_markup=kb
    )


@router.message(Command('subscribers'))
async def cmd_subscribers(message: Message):
    if not is_admin(message.from_user.id):
        return
    if not reminder_subscribers:
        await message.answer("📧 Подписчиков пока нет.")
        return
    subs = "\n".join(f"• `{uid}`" for uid in sorted(reminder_subscribers))
    await message.answer(f"📧 **ПОДПИСЧИКИ** ({len(reminder_subscribers)}):\n\n{subs}", reply_markup=get_admin_keyboard())


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
    await message.answer(f"📋 **ЛОГ (последние {n} строк):**\n\n```\n{last}\n```", reply_markup=get_admin_keyboard())


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
        await message.answer("✅ Ошибок нет!", reply_markup=get_admin_keyboard())
        return
    text = ''.join(errors)
    if len(text) > 4000:
        text = text[-4000:]
    await message.answer(f"❌ **ОШИБКИ** ({len(errors)}):\n\n```\n{text}\n```", reply_markup=get_admin_keyboard())


@router.message(Command('send_tip'))
async def cmd_send_tip(message: Message):
    if not is_admin(message.from_user.id):
        return
    from handlers.reminders import _send_weekly_tips
    await message.answer("📧 Отправляю совет...")
    await _send_weekly_tips(message.bot)
    await message.answer(f"✅ Совет отправлен {len(reminder_subscribers)} подписчикам!", reply_markup=get_admin_keyboard())
