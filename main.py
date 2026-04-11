import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
from handlers.admin_handler import router as admin_router
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

# Гибридная система: база знаний + YandexGPT для сложных вопросов
yandex_service = YandexGPTService()
hybrid_consultant = HybridAgroConsultant()

# Кэш информации о боте
bot_info_cache = {}


@dp.message(Command('menu'))
async def cmd_menu(message: Message):
    """Главное меню с inline-кнопками"""
    keyboard = get_main_menu_keyboard()
    await message.answer(
        "🌱 **Меню Agrio:**\n\n"
        "Выберите культуру или раздел:",
        reply_markup=keyboard
    )


@dp.message(Command('subscribe'))
async def cmd_subscribe(message: Message):
    """Подписка на еженедельные советы"""
    user_id = message.from_user.id
    reminder_subscribers.add(user_id)
    await message.answer(
        "✅ **Вы подписаны на еженедельные советы!**\n\n"
        "Каждый понедельник в 9:00 вы будете получать актуальный совет по огороду.\n\n"
        "Отписаться: /unsubscribe"
    )


@dp.message(Command('unsubscribe'))
async def cmd_unsubscribe(message: Message):
    """Отписка от еженедельных советов"""
    user_id = message.from_user.id
    if user_id in reminder_subscribers:
        reminder_subscribers.discard(user_id)
        await message.answer("❌ Вы отписались от еженедельных советов.")
    else:
        await message.answer("Вы не были подписаны на советы.")


def get_chat_mode(chat_id: int) -> str:
    """
    Определить режим работы бота для чата.

    Returns:
        "mention" - отвечать только по упоминанию
        "agro" - отвечать на все сообщения (режим агронома)
        "unknown" - чат не настроен
    """
    if chat_id == CHAT_MENTION_ONLY:
        return "mention"
    elif chat_id == CHAT_AGRO_MODE:
        return "agro"
    return "unknown"


@dp.message(~F.text.startswith('/'))
async def handle_all_messages(message: Message, state: FSMContext):
    """Обработчик всех сообщений — делегирует в user_messages"""
    chat_id = message.chat.id
    chat_type = message.chat.type

    # Проверка: разрешён ли этот чат
    if PRIVATE_CHATS:
        if chat_id not in PRIVATE_CHATS:
            logger.warning(f"Чат {chat_id} не в списке разрешённых!")
            return

    # Определяем режим работы для этого чата
    chat_mode = get_chat_mode(chat_id)

    # Определяем, является ли чат групповым
    is_group = chat_type in ["group", "supergroup", "channel"]

    # Передаём обработку
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
    """Запуск бота"""
    try:
        # Регистрация ВСЕХ роутеров
        dp.include_router(commands_router)
        dp.include_router(catalog_router)
        dp.include_router(tip_router)
        dp.include_router(stats_router)
        dp.include_router(photo_router)
        dp.include_router(belarusian_router)
        dp.include_router(admin_router)
        dp.include_router(weather_router)

        bot_info = await bot.get_me()
        logger.info(f"Бот авторизован: @{bot_info.username} (ID: {bot_info.id})")

        # Кэшируем информацию о боте
        bot_info_cache["username"] = bot_info.username
        bot_info_cache["id"] = bot_info.id

        # Запуск планировщика напоминаний
        asyncio.create_task(start_reminder_scheduler(bot))
        logger.info("Планировщик напоминаний запущен")

        logger.info("Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        raise
    finally:
        # Закрываем сессии сервисов и бота
        await yandex_service.close()
        await bot.session.close()
        logger.info("Бот остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
