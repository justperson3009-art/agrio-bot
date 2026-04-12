import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config import BOT_TOKEN, ALLOWED_CHATS, CHAT_MENTION_ONLY, CHAT_AGRO_MODE, PRIVATE_CHATS
from ai_yandex import YandexGPTService
from hybrid_ai import HybridAgroConsultant

# Импорт роутеров
from handlers.commands import router as commands_router
from handlers.catalog_handler import router as catalog_router
from handlers.user_messages import handle_user_message

# Новые модули
from handlers.tip_handler import router as tip_router
from handlers.stats_handler import router as stats_router
from handlers.photo_handler import router as photo_router
from handlers.belarusian import router as belarusian_router
# from handlers.admin_handler import router as admin_router  # НЕ используется, кнопки в main.py
from handlers.weather_handler import router as weather_router
from handlers.reminders import start_reminder_scheduler, reminder_subscribers
from keyboards.inline_menus import (
    get_main_menu_keyboard,
    get_crop_submenu_keyboard,
    get_back_to_main_keyboard,
    get_month_keyboard,
    get_yes_no_keyboard
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Гибридная система
yandex_service = YandexGPTService()
hybrid_consultant = HybridAgroConsultant()

# Кэш информации о боте
bot_info_cache = {}

# Админские кнопки (обрабатываются здесь, не в роутере)
ADMIN_BUTTONS = {
    "📊 Статистика", "📧 Подписчики", "📢 Рассылка",
    "❌ Ошибки", "📋 Лог", "💡 Совет всем",
    "🙈 Скрыть меню", "❌ Отменить рассылку"
}

# Простое состояние рассылки
broadcast_mode = {}  # user_id -> True если в режиме рассылки


@dp.message(Command('menu'))
async def cmd_menu(message: Message):
    keyboard = get_main_menu_keyboard()
    await message.answer(
        "🌱 **Меню Agrio:**\n\n"
        "Выберите культуру или раздел:",
        reply_markup=keyboard
    )


@dp.message(Command('subscribe'))
async def cmd_subscribe(message: Message):
    user_id = message.from_user.id
    reminder_subscribers.add(user_id)
    await message.answer(
        "✅ **Вы подписаны на еженедельные советы!**\n\n"
        "Каждый понедельник в 9:00 вы будете получать актуальный совет.\n\n"
        "Отписаться: /unsubscribe"
    )


@dp.message(Command('unsubscribe'))
async def cmd_unsubscribe(message: Message):
    user_id = message.from_user.id
    if user_id in reminder_subscribers:
        reminder_subscribers.discard(user_id)
        await message.answer("❌ Вы отписались от рассылки.")
    else:
        await message.answer("Вы не были подписаны.")


def get_chat_mode(chat_id: int) -> str:
    if chat_id == CHAT_MENTION_ONLY:
        return "mention"
    elif chat_id == CHAT_AGRO_MODE:
        return "agro"
    return "unknown"


def is_admin(user_id: int) -> bool:
    """Проверка: является ли пользователь админом"""
    from config import ADMIN_ID
    if ADMIN_ID and user_id == int(ADMIN_ID):
        return True
    return False


async def handle_admin_button(message: Message):
    """Обработка нажатий админских кнопок"""
    from handlers.admin_handler import (
        get_admin_kb, _autodel, reminder_subscribers
    )
    from handlers.reminders import _send_weekly_tips
    
    user_id = message.from_user.id
    text = message.text
    
    logger.info(f"АДМИНСКАЯ КНОПКА: '{text}' от user_id={user_id}")
    
    # Проверка админа
    if not is_admin(user_id):
        logger.warning(f"Попытка доступа к админке от user_id={user_id}")
        sent = await message.answer("⛔ У вас нет прав администатора.")
        await _autodel(sent, 5)
        return True  # Обработано
    
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
        broadcast_mode[user_id] = True
        await message.answer(
            "📢 **Режим рассылки**\n\n"
            "Просто напишите текст — он будет отправлен всем подписчикам.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отменить рассылку")]],
                resize_keyboard=True
            )
        )

    elif text == "❌ Отменить рассылку":
        broadcast_mode.pop(user_id, None)
        sent = await message.answer("📢 Рассылка отменена.", reply_markup=get_admin_kb())
        await _autodel(sent, 5)

    elif text == "💡 Совет всем":
        status = await message.answer("📧 Отправляю совет подписчикам...")
        try:
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
    
    return True  # Кнопка обработана


@dp.message(F.text.in_(ADMIN_BUTTONS))
async def catch_admin_buttons(message: Message):
    """Перехват админских кнопок ДО общего обработчика"""
    logger.info(f"Перехвачена кнопка: '{message.text}' от user_id={message.from_user.id}")
    await handle_admin_button(message)


@dp.message(~F.text.startswith('/'))
async def handle_all_messages(message: Message, state: FSMContext):
    """Обработчик всех сообщений (НЕ команды и НЕ админские кнопки)"""
    user_id = message.from_user.id
    
    # Проверка: режим рассылки?
    if user_id in broadcast_mode and is_admin(user_id):
        text = message.text.strip()
        if text:
            from handlers.reminders import reminder_subscribers
            from handlers.admin_handler import get_admin_kb, _autodel
            
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
            try:
                await message.bot.delete_message(message.chat.id, status.message_id)
            except:
                pass
            sent = await message.answer("✅ Рассылка завершена.", reply_markup=get_admin_kb())
            await _autodel(sent, 5)
            broadcast_mode.pop(user_id, None)
        return

    chat_id = message.chat.id
    chat_type = message.chat.type

    # Проверка: разрешён ли этот чат
    if PRIVATE_CHATS:
        if chat_id not in PRIVATE_CHATS:
            return

    chat_mode = get_chat_mode(chat_id)
    is_group = chat_type in ["group", "supergroup", "channel"]

    await handle_user_message(
        message=message,
        state=state,
        hybrid_consultant=hybrid_consultant,
        yandex_service=yandex_service,
        bot_info_cache=bot_info_cache,
        chat_mode=chat_mode,
        is_group=is_group
    )


async def main():
    try:
        # === ПОРЯДОК ВАЖЕН! ===
        dp.include_router(commands_router)    # 1. Команды
        dp.include_router(catalog_router)     # 2. Каталог
        dp.include_router(tip_router)         # 3. Совет дня
        dp.include_router(stats_router)       # 4. Статистика
        dp.include_router(photo_router)       # 5. Фото
        dp.include_router(belarusian_router)  # 6. Белорусский
        dp.include_router(weather_router)     # 7. Погода
        # Админские кнопки обрабатываются catch_admin_buttons() выше

        bot_info = await bot.get_me()
        logger.info(f"Бот авторизован: @{bot_info.username} (ID: {bot_info.id})")

        bot_info_cache["username"] = bot_info.username
        bot_info_cache["id"] = bot_info.id

        # Планировщик напоминаний
        asyncio.create_task(start_reminder_scheduler(bot))
        logger.info("Планировщик напоминаний запущен")

        logger.info("Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        raise
    finally:
        await yandex_service.close()
        await bot.session.close()
        logger.info("Бот остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
