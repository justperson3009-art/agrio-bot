import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
ALLOWED_CHAT_IDS = os.getenv("ALLOWED_CHAT_IDS") or ""

# Qwen API (облако Alibaba DashScope)
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

# Локальная Qwen модель (Ollama)
QWEN_LOCAL = os.getenv("QWEN_LOCAL", "false").lower() == "true"
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen2.5:7b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# Проверка: либо QWEN_API_KEY для облака, либо QWEN_LOCAL=true для локальной версии
if not QWEN_API_KEY and not QWEN_LOCAL:
    raise ValueError("QWEN_API_KEY не найден И QWEN_LOCAL не установлен в true")

# Список разрешённых chat_id (через запятую) или пустой = все чаты разрешены
if ALLOWED_CHAT_IDS and ALLOWED_CHAT_IDS.strip():
    ALLOWED_CHATS = [int(x.strip()) for x in ALLOWED_CHAT_IDS.split(",") if x.strip()]
else:
    ALLOWED_CHATS = None  # Все чаты разрешены

# ==========================================
# НАСТРОЙКИ ЧАТОВ (для экономии токенов)
# ==========================================
# ЧАТ 1: Отвечает только по упоминанию @bot
# ЧАТ 2: Отвечает на все сообщения (режим агронома)
# ==========================================

# Chat ID чата где бот отвечает ТОЛЬКО по упоминанию
CHAT_MENTION_ONLY = int(os.getenv("CHAT_MENTION_ONLY") or "0")

# Chat ID чата где бот отвечает НА ВСЕ сообщения (режим агронома)
CHAT_AGRO_MODE = int(os.getenv("CHAT_AGRO_MODE") or "0")

# Проверка: если оба чата настроены, используем их
PRIVATE_CHATS = []
if CHAT_MENTION_ONLY and CHAT_MENTION_ONLY != 0:
    PRIVATE_CHATS.append(CHAT_MENTION_ONLY)
if CHAT_AGRO_MODE and CHAT_AGRO_MODE != 0 and CHAT_AGRO_MODE != CHAT_MENTION_ONLY:
    PRIVATE_CHATS.append(CHAT_AGRO_MODE)
