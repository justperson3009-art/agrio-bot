from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню бота."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🍅 Томаты и перцы", callback_data="menu:tomatoes"))
    builder.row(InlineKeyboardButton(text="🥒 Огурцы и кабачки", callback_data="menu:cucumbers"))
    builder.row(InlineKeyboardButton(text="🥬 Капуста и зелень", callback_data="menu:cabbage"))
    builder.row(InlineKeyboardButton(text="🥕 Корнеплоды", callback_data="menu:roots"))
    builder.row(InlineKeyboardButton(text="🌳 Деревья и ягоды", callback_data="menu:trees"))
    builder.row(InlineKeyboardButton(text="🌾 Зерновые и травы", callback_data="menu:grains"))
    builder.row(InlineKeyboardButton(text="💡 Совет дня", callback_data="menu:tip"))
    builder.row(InlineKeyboardButton(text="🗓️ Календарь работ", callback_data="menu:calendar"))
    builder.row(InlineKeyboardButton(text="🤝 Совместимость", callback_data="menu:compatibility"))
    builder.row(InlineKeyboardButton(text="🌙 Лунный календарь", callback_data="menu:lunar"))
    return builder.as_markup()


def get_crop_submenu_keyboard(crop_type: str) -> InlineKeyboardMarkup:
    """Подменю для конкретной культуры."""
    builder = InlineKeyboardBuilder()

    crop_menus = {
        "tomatoes": {
            "items": [
                ("🌱 Рассада", "crop:tomato:seedling"),
                ("💧 Полив", "crop:tomato:watering"),
                ("🥄 Подкормка", "crop:tomato:feeding"),
                ("🐛 Болезни", "crop:tomato:diseases"),
                ("⚠️ Проблемы", "crop:tomato:problems"),
            ],
            "label": "tomato",
        },
        "cucumbers": {
            "items": [
                ("🌱 Рассада", "crop:cucumber:seedling"),
                ("💧 Полив", "crop:cucumber:watering"),
                ("🥄 Подкормка", "crop:cucumber:feeding"),
                ("🐛 Болезни", "crop:cucumber:diseases"),
                ("⚠️ Проблемы", "crop:cucumber:problems"),
            ],
            "label": "cucumber",
        },
        "cabbage": {
            "items": [
                ("🌱 Рассада", "crop:cabbage:seedling"),
                ("💧 Полив", "crop:cabbage:watering"),
                ("🥄 Подкормка", "crop:cabbage:feeding"),
                ("🐛 Болезни", "crop:cabbage:diseases"),
                ("⚠️ Проблемы", "crop:cabbage:problems"),
            ],
            "label": "cabbage",
        },
        "roots": {
            "items": [
                ("🥕 Морковь", "crop:carrot:info"),
                ("🟤 Свёкла", "crop:beet:info"),
                ("🥔 Картофель", "crop:potato:info"),
                ("💧 Полив", f"crop:roots:watering"),
                ("🥄 Подкормка", f"crop:roots:feeding"),
                ("🐛 Болезни", f"crop:roots:diseases"),
            ],
            "label": "roots",
        },
        "trees": {
            "items": [
                ("🍎 Яблоня", "crop:apple:info"),
                ("🍐 Груша", "crop:pear:info"),
                ("🍒 Вишня", "crop:cherry:info"),
                ("✂️ Обрезка", "crop:trees:pruning"),
                ("🐛 Болезни", "crop:trees:diseases"),
            ],
            "label": "trees",
        },
        "grains": {
            "items": [
                ("🌾 Пшеница", "crop:wheat:info"),
                ("🌽 Кукуруза", "crop:corn:info"),
                ("🌻 Подсолнечник", "crop:sunflower:info"),
                ("💧 Полив", "crop:grains:watering"),
                ("🥄 Подкормка", "crop:grains:feeding"),
            ],
            "label": "grains",
        },
    }

    crop = crop_menus.get(crop_type)
    if not crop:
        crop = crop_menus["tomatoes"]

    for text, callback in crop["items"]:
        builder.row(InlineKeyboardButton(text=text, callback_data=callback))

    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="back:main"))
    return builder.as_markup()


def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Кнопка «Назад» в главное меню."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="back:main"))
    return builder.as_markup()


def get_month_keyboard(month_num: int) -> InlineKeyboardMarkup:
    """Клавиатура выбора месяца (1–12 в 3 ряда по 4 кнопки)."""
    month_names = [
        "Январь", "Февраль", "Март", "Апрель",
        "Май", "Июнь", "Июль", "Август",
        "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
    ]

    builder = InlineKeyboardBuilder()
    for i in range(1, 13):
        prefix = "✅ " if i == month_num else ""
        builder.button(
            text=f"{prefix}{month_names[i - 1]}",
            callback_data=f"month:{i}",
        )
    builder.adjust(4, 4, 4)
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="back:main"))
    return builder.as_markup()


def get_yes_no_keyboard(callback_prefix: str) -> InlineKeyboardMarkup:
    """Клавиатура Да/Нет для подтверждений."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да", callback_data=f"{callback_prefix}:yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data=f"{callback_prefix}:no"),
    )
    return builder.as_markup()
