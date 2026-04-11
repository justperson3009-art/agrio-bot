from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import os
from datetime import datetime

router = Router()

@router.message(Command('stats'))
async def cmd_stats(message: Message):
    """Статистика бота"""
    # Basic stats without database
    bot_uptime = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Try to count log entries
    log_count = 0
    if os.path.exists('bot.log'):
        with open('bot.log', 'r', encoding='utf-8') as f:
            log_count = sum(1 for _ in f)
    
    stats_text = (
        "📊 **СТАТИСТИКА БОТА**\n\n"
        f"🟢 Бот работает: {bot_uptime}\n"
        f"📝 Записей в логе: {log_count}\n"
        f"📚 Шаблонов в базе: 149\n"
        f"🔤 Паттернов: 1100+\n"
        f"🌱 Культур: 70+\n\n"
        "🧠 **Умная система:**\n"
        "• 120+ синонимов\n"
        "• 13 fallback тем\n"
        "• Нормализация текста\n\n"
        "💡 ИИ используется только для сложных вопросов!"
    )
    
    await message.answer(stats_text)
