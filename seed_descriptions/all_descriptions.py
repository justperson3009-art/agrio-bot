"""
Объединённый модуль всех описаний сортов
Удобный доступ к описаниям по названию сорта
"""

from seed_descriptions.tomatoes import TOMATO_DESCRIPTIONS
from seed_descriptions.peppers import PEPPER_DESCRIPTIONS
from seed_descriptions.other_crops import (
    CARROT_DESCRIPTIONS,
    CABBAGE_WHITE_DESCRIPTIONS,
    CABBAGE_RED_DESCRIPTIONS,
    CORN_DESCRIPTIONS,
    WATERMELON_DESCRIPTIONS,
    EGGPLANT_DESCRIPTIONS,
    BROCCOLI_DESCRIPTIONS,
    MELON_DESCRIPTIONS,
    ZUCCHINI_DESCRIPTIONS,
    CUCUMBER_DESCRIPTIONS,
    PARSLEY_DESCRIPTIONS,
    RADISH_DESCRIPTIONS,
    BEET_DESCRIPTIONS,
    BEAN_DESCRIPTIONS,
    PUMPKIN_DESCRIPTIONS,
    CAULIFLOWER_DESCRIPTIONS,
)


# Объединяем все описания в один словарь
ALL_SEED_DESCRIPTIONS = {}
ALL_SEED_DESCRIPTIONS.update(TOMATO_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(PEPPER_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(CARROT_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(CABBAGE_WHITE_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(CABBAGE_RED_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(CORN_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(WATERMELON_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(EGGPLANT_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(BROCCOLI_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(MELON_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(ZUCCHINI_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(CUCUMBER_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(PARSLEY_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(RADISH_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(BEET_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(BEAN_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(PUMPKIN_DESCRIPTIONS)
ALL_SEED_DESCRIPTIONS.update(CAULIFLOWER_DESCRIPTIONS)


def get_seed_description(seed_name: str) -> dict | None:
    """
    Получить описание сорта по названию.

    Args:
        seed_name: Название сорта (например "СУПЕРНОВА F1")

    Returns:
        Словарь с описанием или None если сорт не найден
    """
    name_upper = seed_name.upper().strip()
    return ALL_SEED_DESCRIPTIONS.get(name_upper)


def get_all_descriptions() -> dict:
    """Получить все описания"""
    return ALL_SEED_DESCRIPTIONS


def get_description_count() -> int:
    """Количество описанных сортов"""
    return len(ALL_SEED_DESCRIPTIONS)
