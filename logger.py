import logging
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

LOG_FILE = Path("logs/ai_requests.log")


def ensure_log_dir():
    """Создать директорию для логов если не существует"""
    LOG_FILE.parent.mkdir(exist_ok=True)


def log_ai_request(user_id: int, username: str, question: str, answer: str, tokens_used: int = 0):
    """
    Логирование запроса к ИИ.
    
    Args:
        user_id: ID пользователя
        username: Имя пользователя
        question: Вопрос пользователя
        answer: Ответ ИИ
        tokens_used: Количество использованных токенов (опционально)
    """
    ensure_log_dir()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "username": username,
        "question": question[:200],  # Обрезаем длинные вопросы
        "answer_length": len(answer),
        "tokens_used": tokens_used
    }
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        logger.info(f"Запрос к ИИ залогирован: user_id={user_id}")
    except Exception as e:
        logger.error(f"Ошибка при логировании: {e}")
