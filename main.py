import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN, ALLOWED_CHATS, CHAT_MENTION_ONLY, CHAT_AGRO_MODE, PRIVATE_CHATS
from ai_yandex import YandexGPTService
from hybrid_ai import HybridAgroConsultant
from moderation import moderate_message
from logger import log_ai_request
from seeds_database import seeds_db

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

# Хранилище контекста диалога для каждого пользователя
user_dialogs = {}

# Кэш информации о боте
bot_info_cache = {}


class ConsultationStates(StatesGroup):
    """FSM состояния для консультации"""
    waiting_for_question = State()


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


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "🌱 Привет! Я Agrio-Бот, ваш виртуальный агроном-консультант.\n\n"
        "🏪 **AGRIO.BY** — магазин качественных семян\n\n"
        "📚 **Я помогаю с:**\n"
        "• Посадкой и выращиванием растений\n"
        "• Уходом за рассадой\n"
        "• Выбором сортов\n"
        "• Агротехникой\n\n"
        "🛒 **Где купить семена AGRIO:**\n"
        "🌐 Сайт: agrio.by\n"
        "📦 Ozon: ozon.by/seller/agrio/\n"
        "📦 Wildberries: wildberries.kg/seller/4182657\n\n"
        "💡 Задайте мне вопрос о растениях или используйте /catalog для просмотра всех семян!"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "📚 **Команды бота:**\n\n"
        "/start - Начать общение\n"
        "/help - Показать эту справку\n"
        "/catalog - Показать ВСЕ семена AGRIO по категориям\n"
        "/about - О проекте Agrio\n"
        "/status - Проверить состояние бота\n\n"
        "💡 **Как использовать:**\n"
        "• В личных чатах: просто пишите вопрос\n"
        "• В группах: упоминайте бота @Agrio_Bot\n\n"
        "🌱 **Примеры запросов:**\n"
        "• «Когда сажать томаты на рассаду?»\n"
        "• «Какие томаты лучше для теплицы?»\n"
        "• «Посоветуй ранний перец»\n"
        "• «Как ухаживать за баклажанами?»\n"
        "• «Какие сорта у вас есть?»\n\n"
        "📋 **Команда «Каталог»:**\n"
        "Просто напишите **«Каталог»** или **«Коталог»** (даже с опечаткой!)\n"
        "Бот покажет все 104 сорта семян по категориям!\n\n"
        "🛒 **Где купить:**\n"
        "• «Где купить семена?»\n"
        "• «Есть ли у вас сайт?»\n"
        "• «Как заказать?»"
    )


@dp.message(Command("about"))
async def cmd_about(message: Message):
    """Обработчик команды /about"""
    await message.answer(
        "🏪 **Agrio** — интернет-магазин семян в Беларуси.\n\n"
        "📍 **Адрес:** аг. Ольшаны, Столинский район, Брестская область\n"
        "📞 **Телефон:** +375 29 795 99 68\n\n"
        "🌱 **В ассортименте:**\n"
        "• Томаты (29 гибридов)\n"
        "• Перец (13 сортов)\n"
        "• Морковь, капуста, арбузы\n"
        "• Кабачки, тыквы, брокколи\n"
        "• Дыни, баклажаны и др.\n\n"
        "Я — ИИ-консультант, созданный чтобы помогать вам с вопросами о растениях и подборе семян.\n\n"
        "🌐 **Сайт:** agrio.by\n"
        "💡 Если я не могу помочь, наша служба поддержки всегда на связи!"
    )


@dp.message(Command("status"))
async def cmd_status(message: Message):
    """Обработчик команды /status - проверка состояния бота"""
    bot_info = await bot.get_me()

    status_text = (
        "🔍 **Статус бота**\n\n"
        f"🤖 Имя: {bot_info.first_name}\n"
        f"📛 Username: @{bot_info.username}\n"
        f"🆔 ID: {bot_info.id}\n\n"
        f"✅ Бот работает\n\n"
        "📋 **Настройки приватности:**\n"
        f"• Может присоединяться к группам: {'✅' if bot_info.can_join_groups else '❌'}\n"
        f"• Читает все сообщения в группе: {'✅' if bot_info.can_read_all_group_messages else '❌'}\n\n"
        "⚠️ **Если 'Читает все сообщения' = ❌:**\n"
        "1. Напишите @BotFather\n"
        "2. /setprivacy → выберите бота → Disable\n"
        "3. Удалите бота из группы и добавьте снова"
    )

    await message.answer(status_text)


@dp.message(Command("catalog"))
async def cmd_catalog(message: Message):
    """Обработчик команды /catalog - показать ВСЕ семена по категориям"""
    
    # Получаем все семена из базы
    all_seeds = seeds_db.seeds
    
    # Группируем по категориям
    categories = {}
    for seed in all_seeds:
        cat = seed.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(seed)
    
    # Формируем ответ по категориям
    result = "🌱 **ВСЕ СЕМЕНА AGRIO.BY**\n\n"
    
    # Порядок категорий
    category_order = [
        ("томат", "🍅 ТОМАТЫ"),
        ("перец", "🌶️ ПЕРЕЦ"),
        ("морковь", "🥕 МОРКОВЬ"),
        ("капуста белокочанная", "🥬 КАПУСТА"),
        ("арбуз", "🍉 АРБУЗ"),
        ("кабачок", "🥒 КАБАЧОК"),
        ("тыква", "🎃 ТЫКВА"),
        ("брокколи", "🥦 БРОККОЛИ"),
        ("дыня", "🍈 ДЫНЯ"),
        ("баклажан", "🍆 БАКЛАЖАН"),
        ("кукуруза сахарная", "🌽 КУКУРУЗА"),
        ("цветная капуста", "🥬 ЦВЕТНАЯ КАПУСТА"),
        ("петрушка", "🌿 ПЕТРУШКА"),
        ("редис", "🔴 РЕДИС"),
        ("свекла столовая", "🔴 СВЕКЛА"),
        ("спаржевая фасоль", "🫘 ФАСОЛЬ"),
    ]
    
    for cat_key, cat_name in category_order:
        if cat_key in categories:
            result += f"\n{cat_name} ({len(categories[cat_key])}):\n"
            for seed in categories[cat_key]:
                result += f"• **{seed.name}**"
                if seed.ripening_period:
                    result += f" ({seed.ripening_period})"
                if seed.fruit_weight:
                    result += f" {seed.fruit_weight}"
                result += "\n"
    
    # Остальные категории
    processed = [c[0] for c in category_order]
    for cat_key in categories:
        if cat_key not in processed:
            result += f"\n{cat_key.upper()} ({len(categories[cat_key])}):\n"
            for seed in categories[cat_key]:
                result += f"• **{seed.name}**\n"
    
    result += "\n🛒 **Где купить:**\n"
    result += "🌐 agrio.by | 📦 ozon.by/seller/agrio/ | 📦 WB: wildberries.kg/seller/4182657\n\n"
    result += "💡 Спросите меня о любом сорте — дам инструкцию по посадке!"
    
    await message.answer(result)


def is_bot_mentioned(message: Message) -> bool:
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
            # mention - текстовое упоминание @username
            if entity.type == "mention":
                mention_text = message.text[entity.offset:entity.offset + entity.length]
                if mention_text.lower() == f"@{bot_username}".lower():
                    return True
            elif entity.type == "text_mention":
                # text_mention всегда означает упоминание бота, если entity.user == bot
                if entity.user and entity.user.id == bot_info_cache.get("id"):
                    return True

    return False


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


def get_catalog_response() -> str:
    """Готовый ответ о всех сортах семян AGRIO"""
    all_seeds = seeds_db.seeds
    
    # Группируем по категориям
    categories = {}
    for seed in all_seeds:
        cat = seed.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(seed)
    
    # Формируем ответ
    result = "🌱 **ВСЕ СЕМЕНА AGRIO.BY (104 сорта)**\n\n"
    
    category_order = [
        ("томат", "🍅 ТОМАТЫ", 29),
        ("перец", "🌶️ ПЕРЕЦ", 13),
        ("морковь", "🥕 МОРКОВЬ", 7),
        ("капуста белокочанная", "🥬 КАПУСТА", 8),
        ("арбуз", "🍉 АРБУЗ", 7),
        ("кабачок", "🥒 КАБАЧОК", 7),
        ("тыква", "🎃 ТЫКВА", 7),
        ("брокколи", "🥦 БРОККОЛИ", 7),
        ("дыня", "🍈 ДЫНЯ", 7),
        ("баклажан", "🍆 БАКЛАЖАН", 3),
        ("кукуруза сахарная", "🌽 КУКУРУЗА", 2),
        ("цветная капуста", "🥬 ЦВЕТНАЯ КАПУСТА", 2),
        ("петрушка", "🌿 ПЕТРУШКА", 1),
        ("редис", "🔴 РЕДИС", 1),
        ("свекла столовая", "🔴 СВЕКЛА", 1),
        ("спаржевая фасоль", "🫘 ФАСОЛЬ", 2),
    ]
    
    for cat_key, cat_name, _ in category_order:
        if cat_key in categories:
            result += f"\n{cat_name}:\n"
            for seed in categories[cat_key]:
                result += f"• **{seed.name}**\n"
    
    result += "\n🛒 **Где купить:**\n"
    result += "🌐 agrio.by | 📦 ozon.by/seller/agrio/ | 📦 WB: wildberries.kg/seller/4182657\n\n"
    result += "💡 Спросите меня о любом сорте — дам инструкцию по посадке!"
    
    return result


def is_catalog_question(text: str) -> bool:
    """Проверка: пользователь спрашивает про ассортимент семян?"""
    catalog_keywords = [
        'какие сорт', 'какие семен', 'какие растени', 'ассортимент',
        'что есть', 'что у вас', 'список сорт', 'полный список',
        'все сорт', 'все семен', 'каталог', 'номенклатур'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in catalog_keywords)


def is_catalog_command(text: str) -> bool:
    """Проверка: команда 'Каталог' (в т.ч. с опечаткой 'Коталог')"""
    text_lower = text.lower().strip()
    # Точное совпадение или с опечаткой
    return text_lower in ['каталог', 'коталог', 'каталог семян', 'коталог семян']


@dp.message(F.text.lower().regexp(r'^(каталог|коталог)(\s*семян)?$'))
async def cmd_catalog_text(message: Message):
    """Обработчик команды 'Каталог' (в т.ч. с опечаткой 'Коталог')"""
    await message.answer(get_catalog_response())


async def handle_user_message(message: Message, state: FSMContext):
    """Обработчик сообщений от пользователя (гибридная система)"""
    user_text = message.text
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"
    chat_id = message.chat.id
    chat_type = message.chat.type

    logger.info(f"=== ВХОДЯЩЕЕ СООБЩЕНИЕ ===")
    logger.info(f"От: {username} (user_id={user_id})")
    logger.info(f"Чат: {chat_id}, тип: {chat_type}")
    logger.info(f"Текст: {user_text[:100]}")
    logger.info(f"Bot username: @{bot_info_cache.get('username')}")

    # Проверка: разрешён ли этот чат
    if PRIVATE_CHATS:
        if chat_id not in PRIVATE_CHATS:
            logger.warning(f"Чат {chat_id} не в списке разрешённых!")
            return

    # Определяем режим работы для этого чата
    chat_mode = get_chat_mode(chat_id)
    logger.info(f"Режим чата: {chat_mode}")

    # Если группа или mention_only — проверяем упоминание бота
    is_group = message.chat.type in ["group", "supergroup", "channel"]

    if is_group or chat_mode == "mention":
        mentioned = is_bot_mentioned(message)
        logger.info(f"Бот упомянут: {mentioned}")

        if not mentioned:
            logger.info(f"Бот не упомянут — игнорируем")
            return

        # Удаляем упоминание бота из текста
        bot_username = f"@{bot_info_cache.get('username')}"
        user_text = user_text.replace(bot_username, "").strip()
        user_text = user_text.replace(bot_username.lower(), "").strip()

        if not user_text or user_text == "?":
            await message.answer(
                "🌱 Задайте мне вопрос о растениях!\n\n"
                "Например: когда сажать томаты?"
            )
            return

    logger.info(f"Чат {chat_id} разрешён, продолжаем обработку...")

    # Проверка модерации
    logger.info(f"Проверка модерации для: {user_text[:50]}")
    is_allowed, reason = moderate_message(user_text)
    if not is_allowed:
        logger.warning(f"Модерация заблокировала сообщение от {username}: {reason}")
        await message.answer(
            "⚠️ Я специалист только по растениям и семенам!\n\n"
            "🏪 **AGRIO.BY** — магазин семян\n"
            "🌐 Сайт: agrio.by\n"
            "📦 Ozon: ozon.by/seller/agrio/\n"
            "📦 WB: wildberries.kg/seller/4182657\n\n"
            "🌱 Задайте вопрос о выращивании растений!"
        )
        return

    logger.info(f"Модерация пройдена")

    # Проверка: команда "Каталог" (в т.ч. с опечаткой "Коталог")
    if is_catalog_command(user_text):
        logger.info("Команда 'Каталог' — отправляем полный каталог")
        await message.answer(get_catalog_response())
        return

    # Проверка: вопрос про ассортимент семян? (готовый ответ без ИИ)
    if is_catalog_question(user_text):
        logger.info("Вопрос про ассортимент — отправляем готовый каталог")
        await message.answer(get_catalog_response())
        return

    # Проверка на prompt injection
    if await ai_consultant.check_injection_attempt(user_text):
        logger.warning(f"Попытка injection от {username}")
        await message.answer(
            "⚠️ Я не могу изменить свои инструкции. "
            "Задайте вопрос о растениях!"
        )
        return

    logger.info(f"Проверка на injection пройдена")

    # Отправляем статус "печатает..."
    await bot.send_chat_action(chat_id=chat_id, action="typing")

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

    # Отправка ответа
    await message.answer(response)
    logger.info(f"Ответ отправлен пользователю (источник: {source})")


async def main():
    """Запуск бота"""
    try:
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
