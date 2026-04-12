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
from handlers.admin_handler import router as admin_router  # Админка теперь через роутер
from handlers.weather_handler import router as weather_router
from handlers.feedback_handler import router as feedback_router  # Обратная связь
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

# Админские кнопки (для перехвата в handle_all_messages)
ADMIN_BUTTONS = {
    "📊 Статистика", "📧 Подписчики", "📢 Рассылка",
    "📝 Жалобы", "❌ Ошибки",
    "❌ Отменить рассылку"
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
    from feedback_db import add_subscriber
    user_id = message.from_user.id
    add_subscriber(user_id)
    reminder_subscribers.add(user_id)  # Для обратной совместимости
    await message.answer(
        "✅ **Вы подписаны на еженедельные советы!**\n\n"
        "Каждый понедельник в 9:00 вы будете получать актуальный совет.\n\n"
        "Отписаться: /unsubscribe"
    )


@dp.message(Command('unsubscribe'))
async def cmd_unsubscribe(message: Message):
    from feedback_db import remove_subscriber
    user_id = message.from_user.id
    remove_subscriber(user_id)
    reminder_subscribers.discard(user_id)
    await message.answer("❌ Вы отписались от рассылки.")


def get_chat_mode(chat_id: int) -> str:
    if chat_id == CHAT_MENTION_ONLY:
        return "mention"
    elif chat_id == CHAT_AGRO_MODE:
        return "agro"
    return "unknown"


@dp.message(~F.text.startswith('/'))
async def handle_all_messages(message: Message, state: FSMContext):
    """Обработчик всех сообщений (НЕ команды и НЕ админские кнопки)"""
    user_id = message.from_user.id
    text = message.text

    # === ПЕРЕХВАТ АДМИНСКИХ КНОПОК ===
    if text in ADMIN_BUTTONS:
        logger.info(f"АДМИН КНОПКА: '{text}' от user_id={user_id}")
        from config import ADMIN_ID
        from handlers.admin_handler import get_admin_kb, _autodel, is_admin as check_admin
        from handlers.reminders import _send_weekly_tips
        from feedback_db import get_stats, get_subscribers_list, get_complaints
        
        if not check_admin(user_id):
            sent = await message.answer("⛔ У вас нет прав.")
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
                f"📧 Подписчиков: **{stats['subscribers']}**\n"
                f"📝 Жалоб: **{stats['complaints_count']}**",
                reply_markup=get_admin_kb(),
                parse_mode="Markdown"
            )
            await _autodel(sent, 20)

        elif text == "📧 Подписчики":
            subs = get_subscribers_list()
            if not subs:
                sent = await message.answer("📧 Подписчиков пока нет.", reply_markup=get_admin_kb())
            else:
                lines = [f"• `{s['user_id']}` (с {s['subscribed_at'][:10]})" for s in subs]
                subs_text = "\n".join(lines)
                if len(subs_text) > 4000:
                    subs_text = subs_text[:3900] + "\n\n...ещё"
                sent = await message.answer(f"📧 **ПОДПИСЧИКИ** ({len(subs)}):\n\n{subs_text}", reply_markup=get_admin_kb(), parse_mode="Markdown")
            await _autodel(sent, 20)

        elif text == "📢 Рассылка":
            broadcast_mode[user_id] = True
            await message.answer(
                "📢 **Режим рассылки** — напишите текст для подписчиков.\nДля отмены: **❌ Отменить рассылку**",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="❌ Отменить рассылку")]],
                    resize_keyboard=True
                )
            )

        elif text == "❌ Отменить рассылку":
            broadcast_mode.pop(user_id, None)
            sent = await message.answer("📢 Рассылка отменена.", reply_markup=get_admin_kb())
            await _autodel(sent, 5)

        elif text == "📝 Жалобы":
            complaints = get_complaints(limit=15)
            if not complaints:
                sent = await message.answer("✅ Жалоб нет!", reply_markup=get_admin_kb())
            else:
                txt = ""
                for c in complaints:
                    txt += f"👤 ID: `{c['user_id']}`\n📝 Запрос: {c['message_text'][:100]}\n❌ Жалоба: {c['comment'][:200]}\n🕐 {c['created_at']}\n\n"
                if len(txt) > 4000:
                    txt = txt[:4000] + "..."
                sent = await message.answer(f"📝 **ЖАЛОБЫ** ({len(complaints)}):\n\n{txt}", reply_markup=get_admin_kb(), parse_mode="Markdown")
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
                    sent = await message.answer(f"❌ **ОШИБКИ** ({len(errors)}):\n\n```\n{txt}\n```", reply_markup=get_admin_kb())
            except:
                sent = await message.answer("📋 Лог не найден.", reply_markup=get_admin_kb())
            await _autodel(sent, 20)
        
        return  # Админская кнопка обработана
    
    # Проверка: режим рассылки?
    if user_id in broadcast_mode:
        from config import ADMIN_ID
        if ADMIN_ID and user_id == int(ADMIN_ID):
            text = text.strip()
            if text:
                from feedback_db import get_subscribers_list
                from handlers.admin_handler import get_admin_kb, _autodel
                
                subscribers = get_subscribers_list()
                sent_count = 0
                fail_count = 0
                status_msg = await message.answer(f"📢 **Рассылка...** 0/{len(subscribers)}")

                for sub in subscribers:
                    try:
                        await message.bot.send_message(sub['user_id'], text)
                        sent_count += 1
                    except Exception as e:
                        fail_count += 1
                        logger.error(f"Рассылка {sub['user_id']}: {e}")
                    if (sent_count + fail_count) % 10 == 0:
                        try:
                            await status_msg.edit_text(f"📢 **Рассылка...** {sent_count + fail_count}/{len(subscribers)}")
                        except:
                            pass

                await status_msg.edit_text(f"✅ **Готово!**\n📢 Отправлено: {sent_count}\n❌ Ошибок: {fail_count}")
                await asyncio.sleep(5)
                try:
                    await message.bot.delete_message(message.chat.id, status_msg.message_id)
                except:
                    pass
                sent = await message.answer("✅ Рассылка завершена.", reply_markup=get_admin_kb())
                await _autodel(sent, 5)
                broadcast_mode.pop(user_id, None)
            return
        else:
            broadcast_mode.pop(user_id, None)

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
        dp.include_router(admin_router)       # 1. Админка
        dp.include_router(feedback_router)    # 2. Обратная связь (callbacks)
        dp.include_router(commands_router)    # 3. Команды
        dp.include_router(catalog_router)     # 4. Каталог
        dp.include_router(tip_router)         # 5. Совет дня
        dp.include_router(stats_router)       # 6. Статистика
        dp.include_router(photo_router)       # 7. Фото
        dp.include_router(belarusian_router)  # 8. Белорусский
        dp.include_router(weather_router)     # 9. Погода

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
