import re
from typing import Optional
from prompts import AGRO_KEYWORDS, STOP_WORDS


def contains_profanity(text: str) -> bool:
    """
    Простая проверка на нецензурную лексику.
    Можно расширить список или подключить внешний API модерации.
    """
    profanity_patterns = [
        r"\b(еб[а-яё]+)\b",
        r"\b(х[ую][а-яё]+)\b",
        r"\b(пизд[а-яё]+)\b",
        r"\b(бля[а-яё]*)\b",
        r"\b(сук[аа][а-яё]*)\b",
    ]
    text_lower = text.lower()
    for pattern in profanity_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False


def is_agro_topic(text: str) -> bool:
    """
    Проверка, относится ли текст к агротематике.
    """
    text_lower = text.lower()
    for keyword in AGRO_KEYWORDS:
        if keyword in text_lower:
            return True
    return False


def contains_offtopic(text: str) -> bool:
    """
    Проверка на оффтоп (запрещённые темы).
    """
    text_lower = text.lower()
    for stop_word in STOP_WORDS:
        if stop_word in text_lower:
            return True
    return False


def moderate_message(text: str) -> tuple[bool, Optional[str]]:
    """
    Модерация сообщения перед отправкой в ИИ.
    
    Returns:
        tuple: (можно_отправлять, причина_отказа)
    """
    if contains_profanity(text):
        return False, "Матерная лексика"
    
    if contains_offtopic(text) and not is_agro_topic(text):
        return False, "Оффтоп"
    
    return True, None
