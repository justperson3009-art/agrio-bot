"""
Модуль ответов для каталога семян
Все тексты и логика формирования каталога здесь

Данные с сайта agrio.by — 93 сорта по 18 категориям
"""

from seeds_database import seeds_db


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
    total = len(all_seeds)
    result = f"🌱 **ВСЕ СЕМЕНА AGRIO.BY ({total} сорта)**\n\n"

    category_order = [
        ("томат", "🍅 ТОМАТЫ", 25),
        ("перец", "🌶️ ПЕРЕЦ", 9),
        ("морковь", "🥕 МОРКОВЬ", 4),
        ("капуста белокочанная", "🥬 КАПУСТА БЕЛОКОЧАННАЯ", 8),
        ("капуста краснокочанная", "🟣 КАПУСТА КРАСНОКОЧАННАЯ", 1),
        ("кукуруза сахарная", "🌽 КУКУРУЗА", 11),
        ("арбуз", "🍉 АРБУЗ", 3),
        ("баклажан", "🍆 БАКЛАЖАН", 3),
        ("брокколи", "🥦 БРОККОЛИ", 3),
        ("дыня", "🍈 ДЫНЯ", 3),
        ("кабачок", "🥒 КАБАЧОК", 3),
        ("огурец", "🥒 ОГУРЕЦ", 3),
        ("петрушка", "🌿 ПЕТРУШКА", 1),
        ("редис", "🔴 РЕДИС", 1),
        ("свекла столовая", "🔴 СВЕКЛА", 1),
        ("спаржевая фасоль", "🫘 ФАСОЛЬ", 3),
        ("тыква", "🎃 ТЫКВА", 7),
        ("цветная капуста", "🥬 ЦВЕТНАЯ КАПУСТА", 4),
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


def get_catalog_inline() -> str:
    """Каталог с подробностями (сроки созревания, вес)"""
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

    category_order = [
        ("томат", "🍅 ТОМАТЫ"),
        ("перец", "🌶️ ПЕРЕЦ"),
        ("морковь", "🥕 МОРКОВЬ"),
        ("капуста белокочанная", "🥬 КАПУСТА БЕЛОКОЧАННАЯ"),
        ("капуста краснокочанная", "🟣 КАПУСТА КРАСНОКОЧАННАЯ"),
        ("кукуруза сахарная", "🌽 КУКУРУЗА"),
        ("арбуз", "🍉 АРБУЗ"),
        ("баклажан", "🍆 БАКЛАЖАН"),
        ("брокколи", "🥦 БРОККОЛИ"),
        ("дыня", "🍈 ДЫНЯ"),
        ("кабачок", "🥒 КАБАЧОК"),
        ("огурец", "🥒 ОГУРЕЦ"),
        ("петрушка", "🌿 ПЕТРУШКА"),
        ("редис", "🔴 РЕДИС"),
        ("свекла столовая", "🔴 СВЕКЛА"),
        ("спаржевая фасоль", "🫘 ФАСОЛЬ"),
        ("тыква", "🎃 ТЫКВА"),
        ("цветная капуста", "🥬 ЦВЕТНАЯ КАПУСТА"),
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

    # Остальные категории (если есть)
    processed = [c[0] for c in category_order]
    for cat_key in categories:
        if cat_key not in processed:
            result += f"\n{cat_key.upper()} ({len(categories[cat_key])}):\n"
            for seed in categories[cat_key]:
                result += f"• **{seed.name}**\n"

    result += "\n🛒 **Где купить:**\n"
    result += "🌐 agrio.by | 📦 ozon.by/seller/agrio/ | 📦 WB: wildberries.kg/seller/4182657\n\n"
    result += "💡 Спросите меня о любом сорте — дам инструкцию по посадке!"

    return result


def is_catalog_command(text: str) -> bool:
    """Проверка: команда 'Каталог' (в т.ч. с опечаткой 'Коталог')"""
    text_lower = text.lower().strip()
    return text_lower in ['каталог', 'коталог', 'каталог семян', 'коталог семян']


def is_catalog_question(text: str) -> bool:
    """Проверка: пользователь спрашивает про ассортимент семян?"""
    catalog_keywords = [
        'какие сорт', 'какие семен', 'какие растени', 'ассортимент',
        'что есть', 'что у вас', 'список сорт', 'полный список',
        'все сорт', 'все семен', 'каталог', 'номенклатур'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in catalog_keywords)
