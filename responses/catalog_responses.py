"""
Модуль ответов для каталога семян
Все тексты и логика формирования каталога здесь
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

    return result


