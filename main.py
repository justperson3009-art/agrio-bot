import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import BOT_TOKEN, ALLOWED_CHATS, CHAT_MENTION_ONLY, CHAT_AGRO_MODE, PRIVATE_CHATS
from ai_yandex import YandexGPTService
from hybrid_ai import HybridAgroConsultant

# Импорт роутеров
from handlers.commands import router as commands_router
from handlers.catalog_handler import router as catalog_router
from handlers.user_messages import handle_user_message

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
        # Регистрация роутеров
        dp.include_router(commands_router)
        dp.include_router(catalog_router)

        bot_info = await bot.get_me()
        logger.info(f"Бот авторизован: @{bot_info.username} (ID: {bot_info.id})")

        # Кэшируем информацию о боте
        bot_info_cache["username"] = bot_info.username
        bot_info_cache["id"] = bot_info.id

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
