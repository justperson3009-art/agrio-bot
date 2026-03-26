import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN, ALLOWED_CHATS, CHAT_MENTION_ONLY, CHAT_AGRO_MODE, PRIVATE_CHATS
from ai_service import AIAgroConsultant
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
ai_consultant = AIAgroConsultant()

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
        "Я помогу вам с вопросами по:\n"
        "• Посадке и выращиванию растений\n"
        "• Уходу за рассадой\n"
        "• Выбору семян\n"
        "• Агротехнике\n\n"
        "Задайте мне любой вопрос о растениях! 🌿\n\n"
        "💡 В личных чатах я отвечаю без упоминаний.\n"
        "👥 В группах — только когда меня упоминают (@Agrio_Bot)."
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "📚 **Команды бота:**\n\n"
        "/start - Начать общение\n"
        "/help - Показать эту справку\n"
        "/about - О проекте Agrio\n"
        "/status - Проверить состояние бота\n"
        "/seeds - Показать каталог семян AGRIO\n"
        "/seed [запрос] - Поиск семян (например: /seed томат)\n\n"
        "💡 **Как использовать:**\n"
        "• В личных чатах: просто пишите вопрос\n"
        "• В группах: упоминайте бота @Agrio_Bot\n\n"
        "🌱 **Примеры запросов:**\n"
        "• «Когда сажать томаты на рассаду?»\n"
        "• «Какие томаты лучше для теплицы?»\n"
        "• «Посоветуй ранний перец»\n"
        "• «Как ухаживать за баклажанами?»\n\n"
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


@dp.message(Command("seeds"))
async def cmd_seeds(message: Message):
    """Обработчик команды /seeds - показать каталог семян"""
    catalog = seeds_db.get_catalog_summary()
    
    catalog_text = (
        f"{catalog}\n\n"
        "🔍 **Поиск семян:**\n"
        "• `/seed томат` — показать все томаты\n"
        "• `/seed СУПЕРНОВА` — найти конкретный сорт\n"
        "• `/seed ранний томат` — поиск по характеристикам\n\n"
        "💡 **Рекомендации:**\n"
        "Просто спросите: «Какие томаты лучше для теплицы?»\n"
        "Или: «Посоветуй ранний перец для открытого грунта»"
    )
    
    await message.answer(catalog_text)


@dp.message(Command("seed"))
async def cmd_seed(message: Message):
    """Обработчик команды /seed - поиск конкретного семени"""
    # Получаем аргумент команды
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "🔍 **Поиск семян**\n\n"
            "Использование:\n"
            "• `/seed томат` — все томаты\n"
            "• `/seed СУПЕРНОВА` — конкретный сорт\n"
            "• `/seed ранний томат` — по характеристикам"
        )
        return
    
    query = args[1]
    
    # Пробуем найти по названию
    seed = seeds_db.get_seed_by_name(query)
    
    if seed:
        # Нашли конкретный сорт
        info = seeds_db.format_seed_info(seed)
        await message.answer(info)
        return
    
    # Если не нашли точное совпадение, ищем по категории или характеристикам
    seeds = seeds_db.search_by_name(query)
    
    if not seeds:
        # Пробуем поиск по категории
        category_seeds = seeds_db.get_seeds_by_category(query)
        if category_seeds:
            seeds = category_seeds[:10]  # Максимум 10
    
    if not seeds:
        # Поиск по характеристикам
        keywords = query.split()
        seeds = seeds_db.search_by_features(keywords)
    
    if seeds:
        if len(seeds) == 1:
            info = seeds_db.format_seed_info(seeds[0])
            await message.answer(info)
        else:
            # Показываем краткий список
            result = f"🔍 **Найдено по запросу «{query}»:**\n\n"
            for i, seed in enumerate(seeds[:10], 1):
                result += f"{i}. **{seed.name}** ({seed.category})\n"
                if seed.ripening_period:
                    result += f"   📅 {seed.ripening_period}"
                if seed.fruit_weight:
                    result += f" | ⚖️ {seed.fruit_weight}"
                result += "\n"
            
            if len(seeds) > 10:
                result += f"\n... и ещё {len(seeds) - 10} сортов\n"
            
            result += "\n💡 Используйте `/seed [название]` для подробной информации"
            await message.answer(result)
    else:
        await message.answer(
            f"❌ Ничего не найдено по запросу «{query}»\n\n"
            "Попробуйте:\n"
            "• Проверить правильность названия\n"
            "• Использовать категорию (томат, перец, морковь)\n"
            "• Запросить рекомендации: «Какие томаты лучше?»"
        )


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


@dp.message(F.text)
async def handle_user_message(message: Message, state: FSMContext):
    """Обработчик сообщений от пользователя"""
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

    # Проверка: разрешён ли этот чат (если PRIVATE_CHATS настроены)
    if PRIVATE_CHATS:
        if chat_id not in PRIVATE_CHATS:
            logger.warning(f"Чат {chat_id} не в списке разрешённых!")
            return  # Игнорируем чат
    
    # Определяем режим работы для этого чата
    chat_mode = get_chat_mode(chat_id)
    logger.info(f"Режим чата: {chat_mode}")

    # Если группа — проверяем упоминание бота
    is_group = message.chat.type in ["group", "supergroup", "channel"]
    
    if is_group or chat_mode == "mention":
        # В группах или в чате mention_only — проверяем упоминание
        mentioned = is_bot_mentioned(message)
        logger.info(f"Бот упомянут: {mentioned}")

        if not mentioned:
            logger.info(f"Бот не упомянут — игнорируем")
            return  # Бот не упомянут — игнорируем

        # Удаляем упоминание бота из текста
        bot_username = f"@{bot_info_cache.get('username')}"
        user_text = user_text.replace(bot_username, "").strip()
        user_text = user_text.replace(bot_username.lower(), "").strip()

        # Если после удаления упоминания текст пустой
        if not user_text or user_text == "?":
            await message.answer(
                "🌱 Задайте мне вопрос о растениях!\n\n"
                "Например: когда сажать томаты?"
            )
            return
    
    logger.info(f"Чат {chat_id} разрешён, продолжаем обработку...")

    # Проверка: это группа или личный чат?
    is_group = message.chat.type in ["group", "supergroup", "channel"]
    logger.info(f"Тип чата: {message.chat.type}, is_group={is_group}")

    # Если группа — проверяем упоминание бота
    if is_group:
        mentioned = is_bot_mentioned(message)
        logger.info(f"Бот упомянут: {mentioned}, entities: {message.entities}")

        if not mentioned:
            logger.info(f"Бот не упомянут в группе — игнорируем")
            # Бот не упомянут — игнорируем
            return

        # Удаляем упоминание бота из текста
        bot_username = f"@{bot_info_cache.get('username')}"
        user_text = user_text.replace(bot_username, "").strip()
        user_text = user_text.replace(bot_username.lower(), "").strip()

        # Если после удаления упоминания текст пустой
        if not user_text or user_text == "?":
            await message.answer(
                "🌱 Задайте мне вопрос о растениях!\n\n"
                "Например: когда сажать томаты?"
            )
            return
    
    logger.info(f"Проверка модерации для: {user_text[:50]}")

    # Проверка на модерацию
    is_allowed, reason = moderate_message(user_text)
    if not is_allowed:
        logger.warning(f"Модерация заблокировала сообщение от {username}: {reason}")
        await message.answer(
            "⚠️ Извините, я специалист только по растениям и семенам. "
            "Не могу ответить на этот вопрос."
        )
        return
    
    logger.info(f"Модерация пройдена")

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
    
    logger.info(f"Отправляем запрос к ИИ...")

    # Получаем контекст диалога
    context = get_user_context(user_id)

    # Запрос к ИИ
    try:
        response = await ai_consultant.get_consultation(user_text, context)
    except Exception as e:
        logger.error(f"Ошибка при получении консультации: {e}")
        response = "Извините, произошла ошибка. Попробуйте позже."

    logger.info(f"Получен ответ от ИИ: {response[:50]}...")

    # Добавляем в контекст
    add_to_context(user_id, "user", user_text)
    add_to_context(user_id, "assistant", response)

    # Логирование
    log_ai_request(user_id, username, user_text, response)

    # Отправка ответа
    await message.answer(response)
    logger.info(f"Ответ отправлен пользователю")


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
        # Закрываем сессию ИИ и бота
        await ai_consultant.close()
        await bot.session.close()
        logger.info("Бот остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
