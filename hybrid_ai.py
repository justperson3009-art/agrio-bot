import logging
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from seeds_database import seeds_db, SeedVariety

logger = logging.getLogger(__name__)


class HybridAgroConsultant:
    """
    Гибридная система консультаций:
    1. Сначала проверяет простые вопросы по базе знаний
    2. Если вопрос сложный — отправляет в YandexGPT
    """

    def __init__(self):
        # Шаблоны простых вопросов с готовыми ответами
        self.simple_patterns = self._init_simple_patterns()
        
        # Ключевые слова для определения категории вопроса
        self.seed_keywords = self._init_seed_keywords()

    def _init_simple_patterns(self) -> dict:
        """Инициализация шаблонов простых вопросов"""
        return {
            # === КОНТАКТЫ И МАГАЗИНЫ ===
            'website': {
                'patterns': ['сайт', 'agrio.by', 'агрио бай', 'агрио.бай'],
                'answer': (
                    "🌐 **Наш сайт:** agrio.by\n\n"
                    "📦 **Интернет-магазин семян:**\n"
                    "• Широкий ассортимент\n"
                    "• Доставка по Беларуси и России\n"
                    "• Гарантия качества"
                )
            },
            'contact': {
                'patterns': ['контакт', 'телефон', 'связаться', 'позвонить', 'написать'],
                'answer': (
                    "📞 **Контакты Agrio:**\n\n"
                    "• Сайт: agrio.by\n"
                    "• Email: info@agrio.by\n"
                    "• Telegram: @agrio_by\n\n"
                    "💬 Мы всегда на связи!"
                )
            },

            # === ДОСТАВКА И ОПЛАТА ===
            'delivery': {
                'patterns': ['доставк', 'доставить', 'пересылк', 'отправк'],
                'answer': (
                    "🚚 **Доставка семян Agrio:**\n\n"
                    "🇧🇾 **Беларусь:**\n"
                    "• Почта — от 3 BYN\n"
                    "• Курьер — от 5 BYN\n\n"
                    "🇷🇺 **Россия:**\n"
                    "• Почта — от 300 RUB\n"
                    "• СДЭК — от 400 RUB\n\n"
                    " Срок: 2-7 дней"
                )
            },
            'payment': {
                'patterns': ['оплат', 'оплатить', 'карта', 'наличн', 'безнал'],
                'answer': (
                    "💳 **Способы оплаты:**\n\n"
                    "• Банковская карта (Visa, MasterCard)\n"
                    "• Электронные кошельки\n"
                    "• Наличные при получении\n"
                    "• Безналичный расчёт (для юр. лиц)"
                )
            },
            'price': {
                'patterns': ['цена', 'стоим', 'сколько стоит', 'прайс', 'дорого', 'дёшево'],
                'answer': (
                    "💰 **Цены на семена Agrio:**\n\n"
                    "• Томаты — от 2.5 BYN / 0.5г\n"
                    "• Перцы — от 3.0 BYN / 0.3г\n"
                    "• Огурцы — от 2.0 BYN / 1г\n"
                    "• Морковь — от 1.5 BYN / 2г\n\n"
                    " **Полный прайс:** agrio.by/price"
                )
            },
            
            # === МАРКЕТПЛЕЙСЫ ===
            'ozon': {
                'patterns': ['озон', 'ozon'],
                'answer': (
                    "📦 **Agrio на Ozon:**\n\n"
                    "🔗 ozon.by/seller/agrio/\n\n"
                    "✅ Быстрая доставка\n"
                    "✅ Гарантия качества\n"
                    "✅ Отзывы покупателей"
                )
            },
            'wildberries': {
                'patterns': ['wildberries', 'вилдберриз', 'wb'],
                'answer': (
                    "📦 **Agrio на Wildberries:**\n\n"
                    "🔗 wildberries.kg/seller/4182657\n\n"
                    "✅ Широкий ассортимент\n"
                    "✅ Пункты выдачи\n"
                    "✅ Возврат"
                )
            },
            
            # === О КОМПАНИИ ===
            'about': {
                'patterns': ['о вас', 'о компании', 'кто вы', 'что такое agrio', 'расскажи про agrio'],
                'answer': (
                    "🌱 **Agrio — профессиональные семена:**\n\n"
                    "✅ 10+ лет на рынке\n"
                    "✅ 500+ сортов в ассортименте\n"
                    "✅ Собственная селекция\n"
                    "✅ Доставка по Беларуси и России\n\n"
                    "🌐 agrio.by"
                )
            },

            # === ПОПУЛЯРНЫЕ ВОПРОСЫ ===
            'when_plant': {
                'patterns': ['когда сажать', 'когда высаживать', 'срок посадки'],
                'answer': (
                    "📅 **Календарь посадки:**\n\n"
                    "• **Март:** Томаты, перцы, баклажаны (на рассаду)\n"
                    "• **Апрель:** Капуста, редис, зелень\n"
                    "• **Май:** Огурцы, кабачки, тыквы\n"
                    "• **Июнь-Июль:** Повторные посевы редиса\n\n"
                    "💡 Уточните культуру для точного совета!"
                )
            },
            'seedling': {
                'patterns': ['рассада', 'рассадой', 'выращивать рассаду'],
                'answer': (
                    "🌱 **Выращивание рассады:**\n\n"
                    "• **Март:** Томаты, перцы, баклажаны\n"
                    "• **Апрель:** Капуста, зелень\n"
                    "• **Май:** Огурцы, кабачки (можно сразу в грунт)\n\n"
                    "💡 Уточните культуру — дам инструкцию!"
                )
            },

            # === РАССАДА: ТОМАТЫ ===
            'tomato_seedling': {
                'patterns': ['рассада томат', 'томаты рассада', 'помидоры рассада', 'рассада помидор', 'выращивать томаты', 'выращивание томатов', 'томаты выращивание', 'как вырастить томат', 'как вырастить томаты', 'как вырастить помидор'],
                'answer': (
                    "🍅 **РАССАДА ТОМАТОВ**\n\n"
                    "📅 **Сроки:** 55-65 дней до высадки\n"
                    "• Ранние: 15-25 марта\n"
                    "• Средние: 1-10 марта\n\n"
                    "🌡️ **Температура:**\n"
                    "• До всходов: +25°C\n"
                    "• После всходов 7 дней: +15°C днём, +12°C ночью\n"
                    "• Далее: +20-22°C днём, +16-18°C ночью\n\n"
                    "💡 **Свет:** 14-16 часов (фитолампа обязательна!)\n\n"
                    "💧 **Полив:**\n"
                    "• До всходов: опрыскивание\n"
                    "• После: под корень, умеренно\n"
                    "• Вода: отстоянная, +20°C\n\n"
                    "🌿 **Пикировка:** 2 настоящих листа, стаканчики 0.5л\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: через 10 дней после пикировки (Нитрофоска 1 ст.л./10л)\n"
                    "• 2-я: через 2 недели (суперфосфат + сульфат калия)\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Вытягивается → меньше воды, больше света, снизить температуру\n"
                    "• Желтеют листья → подкормить азотом\n"
                    "• Фиолетовый оттенок → фосфорное голодание, добавить суперфосфат\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },

            # === РАССАДА: ПЕРЕЦ ===
            'pepper_seedling': {
                'patterns': ['рассада перц', 'перец рассада', 'рассада болгарского перца', 'выращивать перец', 'выращивание перца', 'перец выращивание', 'как вырастить перец', 'как вырастить перцы'],
                'answer': (
                    "🌶️ **РАССАДА ПЕРЦА**\n\n"
                    "📅 **Сроки:** 60-70 дней до высадки\n"
                    "• Ранний: 1-15 февраля\n"
                    "• Средний: 15-28 февраля\n\n"
                    "🌡️ **Температура:**\n"
                    "• До всходов: +28-30°C\n"
                    "• После всходов 5 дней: +16-18°C днём\n"
                    "• Далее: +22-25°C днём, +18-20°C ночью\n\n"
                    "💡 **Свет:** 14-16 часов (досвечивать!)\n\n"
                    "💧 **Полив:**\n"
                    "• Только тёплой водой (+25°C)\n"
                    "• Под корень, не попадать на листья\n"
                    "• Почва всегда слегка влажная\n\n"
                    "🌿 **Пикировка:** НЕ рекомендуется! Перец не любит пересадку\n"
                    "• Сейте сразу в стаканчики 0.5л\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: 2 настоящих листа (Аммофоска 1 ч.л./5л)\n"
                    "• 2-я: через 2 недели (Кемира Люкс)\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Опадают листья → холодно или перелив\n"
                    "• Фиолетовый стебель → нехватка фосфора\n"
                    "• Скручиваются листья → сухой воздух, опрыскивайте\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },

            # === РАССАДА: БАКЛАЖАНЫ ===
            'eggplant_seedling': {
                'patterns': ['рассада баклажан', 'баклажаны рассада', 'синенькие рассада', 'выращивать баклажаны', 'баклажаны выращивание', 'как вырастить баклажан', 'как вырастить баклажаны'],
                'answer': (
                    "🍆 **РАССАДА БАКЛАЖАНОВ**\n\n"
                    "📅 **Сроки:** 60-70 дней до высадки\n"
                    "• Теплица: 15-25 февраля\n"
                    "• Открытый грунт: 1-10 марта\n\n"
                    "🌡️ **Температура:**\n"
                    "• До всходов: +28-30°C\n"
                    "• После всходов: +16-18°C днём, +12-14°C ночью (5 дней)\n"
                    "• Далее: +22-25°C днём, +18-20°C ночью\n\n"
                    "💡 **Свет:** 12-14 часов\n\n"
                    "💧 **Полив:**\n"
                    "• Тёплой водой (+25°C)\n"
                    "• Обильный, но редкий\n"
                    "• Не допускать пересыхания!\n\n"
                    "🌿 **Пикировка:** НЕ рекомендуется\n"
                    "• Сейте в торфяные горшочки 0.5л\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: 10-12 дней после всходов (Кемира Люкс)\n"
                    "• 2-я: через 2 недели (суперфосфат + сульфат калия)\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Вытягивается → мало света\n"
                    "• Желтеют листья → нехватка азота\n"
                    "• Опадают бутоны → перепады температуры\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },

            # === РАССАДА: ОГУРЦЫ ===
            'cucumber_seedling': {
                'patterns': ['рассада огурц', 'огурцы рассада', 'огурцы выращивание', 'выращивать огурцы', 'выращивание огурцов', 'как вырастить огурц', 'как вырастить огурцы'],
                'answer': (
                    "🥒 **РАССАДА ОГУРЦОВ**\n\n"
                    "📅 **Сроки:** 25-30 дней до высадки\n"
                    "• Теплица: 15-20 апреля\n"
                    "• Открытый грунт: 5-10 мая\n\n"
                    "🌡️ **Температура:**\n"
                    "• До всходов: +28-30°C\n"
                    "• После всходов: +18-20°C днём, +15-16°C ночью\n"
                    "• За 3 дня до высадки: снизить до +16°C\n\n"
                    "💡 **Свет:** 10-12 часов\n\n"
                    "💧 **Полив:**\n"
                    "• Тёплой водой (+25°C)\n"
                    "• Почва всегда влажная\n"
                    "• Опрыскивание листьев\n\n"
                    "🌿 **Пикировка:** КАТЕГОРИЧЕСКИ НЕТ!\n"
                    "• Корни не восстанавливаются\n"
                    "• Сейте сразу в стаканчики 0.5л\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: 2 настоящих листа (Нитрофоска 1 ч.л./5л)\n"
                    "• 2-я: через 10 дней (Кемира Люкс)\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Вытягивается → мало света, загущено\n"
                    "• Бледные листья → нехватка азота\n"
                    "• Желтеют нижние → перелив\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },

            # === РАССАДА: КАПУСТА ===
            'cabbage_seedling': {
                'patterns': ['рассада капуст', 'капуста рассада', 'капуста выращивание', 'выращивать капусту', 'выращивание капусты', 'как вырастить капусту'],
                'answer': (
                    "🥬 **РАССАДА КАПУСТЫ**\n\n"
                    "📅 **Сроки:** 35-45 дней до высадки\n"
                    "• Ранняя: 15-25 марта\n"
                    "• Средняя: 1-10 апреля\n"
                    "• Поздняя: 10-20 апреля\n\n"
                    "🌡️ **Температура:**\n"
                    "• До всходов: +20°C\n"
                    "• После всходов 7 дней: +8-10°C днём, +6-8°C ночью\n"
                    "• Далее: +15-18°C днём, +10-12°C ночью\n\n"
                    "💡 **Свет:** 12-14 часов\n\n"
                    "💧 **Полив:**\n"
                    "• Умеренный\n"
                    "• Почва слегка влажная\n"
                    "• Не допускать перелива!\n\n"
                    "🌿 **Пикировка:** Через 7-10 дней после всходов\n"
                    "• Стаканчики 0.3-0.5л\n"
                    "• Заглублять до семядольных листьев\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: через 7 дней после пикировки (Аммиачная селитра)\n"
                    "• 2-я: за 2 недели до высадки (суперфосфат + сульфат калия)\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Чёрная ножка → дезинфицировать почву\n"
                    "• Вытягивается → снизить температуру, больше света\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },

            # === РАССАДА: КАБАЧКИ ===
            'zucchini_seedling': {
                'patterns': ['рассада кабачк', 'кабачки рассада', 'кабачки выращивание', 'выращивать кабачки', 'выращивание кабачков', 'как вырастить кабачок', 'как вырастить кабачки'],
                'answer': (
                    "🥒 **РАССАДА КАБАЧКОВ**\n\n"
                    "📅 **Сроки:** 25-30 дней до высадки\n"
                    "• Теплица: 15-20 апреля\n"
                    "• Открытый грунт: 5-10 мая\n\n"
                    "🌡️ **Температура:**\n"
                    "• До всходов: +25-28°C\n"
                    "• После всходов: +20-22°C днём, +16-18°C ночью\n"
                    "• За неделю до высадки: закаливать\n\n"
                    "💡 **Свет:** 12-14 часов\n\n"
                    "💧 **Полив:**\n"
                    "• Тёплой водой (+25°C)\n"
                    "• Умеренный\n"
                    "• Не попадать на листья\n\n"
                    "🌿 **Пикировка:** НЕТ!\n"
                    "• Сейте в стаканчики 0.5л\n"
                    "• Можно торфяные горшочки\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: 10 дней после всходов (Нитрофоска 1 ст.л./10л)\n"
                    "• 2-я: через 10 дней (органика + зола)\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Вытягивается → мало света\n"
                    "• Бледные листья → нехватка питания\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },

            # === РАССАДА: ТЫКВА ===
            'pumpkin_seedling': {
                'patterns': ['рассада тыкв', 'тыква рассада', 'тыква выращивание', 'выращивать тыкву', 'выращивание тыквы', 'как вырастить тыкву'],
                'answer': (
                    "🎃 **РАССАДА ТЫКВЫ**\n\n"
                    "📅 **Сроки:** 25-30 дней до высадки\n"
                    "• Теплица: 15-20 апреля\n"
                    "• Открытый грунт: 5-10 мая\n\n"
                    "🌡️ **Температура:**\n"
                    "• До всходов: +25-28°C\n"
                    "• После всходов: +18-20°C днём, +15-16°C ночью\n"
                    "• За неделю: закаливать\n\n"
                    "💡 **Свет:** 12-14 часов\n\n"
                    "💧 **Полив:**\n"
                    "• Тёплой водой\n"
                    "• Умеренный\n"
                    "• Почва слегка влажная\n\n"
                    "🌿 **Пикировка:** НЕТ!\n"
                    "• Сейте в стаканчики 0.5л\n"
                    "• Можно торфяные таблетки\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: 10 дней после всходов (Нитрофоска)\n"
                    "• 2-я: через 10 дней (зола + органика)\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Вытягивается → мало света\n"
                    "• Желтеют листья → перелив\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },

            # === РАССАДА: ЗЕЛЕНЬ ===
            'greens_seedling': {
                'patterns': ['рассада зелени', 'петрушка рассада', 'укроп рассада', 'зелень выращивание', 'выращивать зелень', 'выращивание зелени', 'как вырастить зелень', 'как вырастить петрушку', 'как вырастить укроп'],
                'answer': (
                    "🌿 **РАССАДА ЗЕЛЕНИ**\n\n"
                    "📅 **Сроки:**\n"
                    "• Петрушка: 1-15 апреля (30-35 дней)\n"
                    "• Укроп: можно сразу в грунт\n"
                    "• Салат: 15-25 апреля (25-30 дней)\n\n"
                    "🌡️ **Температура:**\n"
                    "• +15-18°C днём, +10-12°C ночью\n"
                    "• Зелень любит прохладу!\n\n"
                    "💡 **Свет:** 12-14 часов\n\n"
                    "💧 **Полив:**\n"
                    "• Умеренный\n"
                    "• Опрыскивание\n"
                    "• Не допускать пересыхания\n\n"
                    "🌿 **Пикировка:**\n"
                    "• Петрушка: можно в кассеты\n"
                    "• Укроп: НЕ пикировать\n"
                    "• Салат: можно в кассеты\n\n"
                    "🥄 **Подкормка:**\n"
                    "• 1-я: через 10 дней (мочевина 1 ч.л./10л)\n"
                    "• 2-я: не требуется\n\n"
                    "⚠️ **Проблемы:**\n"
                    "• Вытягивается → мало света\n"
                    "• Желтеет → перелив\n\n"
                    "💡 Спросите про сорт — дам особенности!"
                )
            },
        }

    def _init_seed_keywords(self) -> dict:
        """Ключевые слова для определения категории семян"""
        return {
            'томат': ['томат', 'помидор', 'томаты', 'помидоры'],
            'перец': ['перец', 'перцы', 'болгарский перец'],
            'огурец': ['огурец', 'огурцы'],
            'морковь': ['морковь', 'морковка'],
            'капуста': ['капуста', 'капусты'],
            'баклажан': ['баклажан', 'баклажаны', 'синенькие'],
            'кабачок': ['кабачок', 'кабачки', 'цукини'],
            'тыква': ['тыква', 'тыквы'],
            'арбуз': ['арбуз', 'арбузы'],
            'дыня': ['дыня', 'дыни'],
            'редис': ['редис', 'редиска'],
            'петрушка': ['петрушка'],
            'укроп': ['укроп'],
            'свекла': ['свекла', 'свёкла'],
            'кукуруза': ['кукуруза'],
            'фасоль': ['фасоль'],
            'горох': ['горох'],
            'лук': ['лук'],
            'чеснок': ['чеснок'],
        }

    def is_simple_question(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Проверка: простой ли вопрос?
        Возвращает: (is_simple, category)
        
        Сначала проверяем конкретные шаблоны (рассада культур),
        потом общие (рассада, когда сажать).
        """
        message_lower = message.lower()
        
        # Сначала проверяем конкретные шаблоны рассады
        specific_categories = [
            'tomato_seedling', 'pepper_seedling', 'eggplant_seedling',
            'cucumber_seedling', 'cabbage_seedling', 'zucchini_seedling',
            'pumpkin_seedling', 'greens_seedling'
        ]
        
        for cat in specific_categories:
            data = self.simple_patterns.get(cat, {})
            for pattern in data.get('patterns', []):
                if pattern in message_lower:
                    logger.debug(f"Найден конкретный вопрос: {cat}")
                    return True, cat
        
        # Потом общие шаблоны
        general_categories = [
            'website', 'contact', 'delivery', 'payment', 'price',
            'ozon', 'wildberries', 'about', 'when_plant', 'seedling'
        ]
        
        for cat in general_categories:
            data = self.simple_patterns.get(cat, {})
            for pattern in data.get('patterns', []):
                if pattern in message_lower:
                    logger.debug(f"Найден общий вопрос: {cat}")
                    return True, cat
        
        return False, None

    def get_simple_answer(self, category: str) -> Optional[str]:
        """Получить готовый ответ для простого вопроса"""
        if category in self.simple_patterns:
            return self.simple_patterns[category]['answer']
        return None

    def is_seed_question(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Проверка: вопрос о семенах/сортах?
        Возвращает: (is_seed_question, category)
        """
        message_lower = message.lower()
        
        for category, keywords in self.seed_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    logger.debug(f"Вопрос о семенах: {category}")
                    return True, category
        
        # Проверка на общие запросы о семенах
        general_seed_words = ['семян', 'семена', 'семен', 'сорт', 'сорта', 'урожай']
        if any(word in message_lower for word in general_seed_words):
            return True, 'general'
        
        return False, None

    def get_seed_recommendations(self, message: str, category: str = None) -> Optional[str]:
        """Получить рекомендации по семенам из базы"""
        message_lower = message.lower()
        
        # Если категория не определена, пытаемся определить
        if not category or category == 'general':
            for cat, keywords in self.seed_keywords.items():
                for keyword in keywords:
                    if keyword in message_lower:
                        category = cat
                        break
                if category:
                    break
        
        # Определение дополнительных критериев
        criteria = {}
        
        if 'ранн' in message_lower:
            criteria['ripening_period'] = 'ранн'
        elif 'средн' in message_lower:
            criteria['ripening_period'] = 'средн'
        elif 'поздн' in message_lower:
            criteria['ripening_period'] = 'поздн'
        
        if 'теплиц' in message_lower:
            criteria['growing_conditions'] = 'теплиц'
        elif 'открыт' in message_lower or 'ог' in message_lower:
            criteria['growing_conditions'] = 'открытый грунт'
        
        if 'хранени' in message_lower:
            criteria['purpose'] = 'хранение'
        elif 'переработ' in message_lower:
            criteria['purpose'] = 'переработка'
        elif 'рынок' in message_lower or 'продаж' in message_lower:
            criteria['purpose'] = 'рынок'
        
        # Поиск в базе
        if category and category != 'general':
            recommendations = seeds_db.get_recommendations_for_category(category, criteria)
            if recommendations:
                return self._format_seed_recommendations(category, recommendations)
        
        # Поиск по ключевым словам
        keywords = message_lower.split()
        search_results = seeds_db.search_by_features(keywords)
        if search_results:
            return self._format_search_results(search_results)
        
        return None

    def _format_seed_recommendations(self, category: str, recommendations: List[SeedVariety]) -> str:
        """Форматирование рекомендаций по семенам"""
        category_name = category.upper().replace('_', ' ')
        result = f"🌱 **Рекомендуемые сорта: {category_name}**\n\n"
        
        for i, seed in enumerate(recommendations[:5], 1):
            result += f"{i}. **{seed.name}** ({seed.variety_type})\n"
            if seed.ripening_period:
                result += f"    {seed.ripening_period}\n"
            if seed.fruit_weight:
                result += f"   ⚖️ {seed.fruit_weight}\n"
            if seed.features:
                for feature in seed.features[:3]:
                    result += f"   • {feature}\n"
            if seed.growing_conditions:
                result += f"    {seed.growing_conditions}\n"
            result += "\n"
        
        result += "💡 Для подробной информации: `/seed [название]`"
        return result

    def _format_search_results(self, results: List[SeedVariety]) -> str:
        """Форматирование результатов поиска"""
        result = " **Найдено в базе семян:**\n\n"
        
        for i, seed in enumerate(results[:5], 1):
            result += f"{i}. **{seed.name}** ({seed.category})\n"
            if seed.ripening_period:
                result += f"   📅 {seed.ripening_period}\n"
            if seed.fruit_weight:
                result += f"   ⚖️ {seed.fruit_weight}\n"
            if seed.description:
                result += f"   {seed.description}\n"
            result += "\n"
        
        result += "💡 Для подробной информации: `/seed [название]`"
        return result

    def is_purchase_request(self, message: str) -> bool:
        """Проверка: запрос о покупке?"""
        purchase_keywords = [
            'купить', 'где найти', 'где приобрести', 'приобрести', 'взять',
            'заказать', 'заказ', 'магазин', 'адрес', 'сайт', 'ссылк',
            'ozon', 'озон', 'доставк', 'оплат', 'цена', 'сколько стоит'
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in purchase_keywords)

    def get_purchase_info(self, message: str) -> str:
        """Информация о покупке без ИИ"""
        info = "🏪 **Где купить семена AGRIO:**\n\n"
        info += "🌐 **Сайт:** agrio.by\n"
        info += "📦 **Ozon:** ozon.by/seller/agrio/\n"
        info += " **Wildberries:** wildberries.kg/seller/4182657\n\n"
        info += "💡 **Доставка:** по всей Беларуси и России\n"
        
        # Семена для текущего месяца
        current_month = datetime.now().month
        month_seeds = self.get_seeds_for_month(current_month)
        
        if month_seeds:
            info += "\n\n **Что сажать в этом месяце:**\n\n"
            for seed in month_seeds[:5]:
                info += f"• **{seed.name}** ({seed.category})\n"
            info += "\n💡 Используйте `/seed [название]` для подробной информации"
        
        return info

    def get_seeds_for_month(self, month: int) -> List[SeedVariety]:
        """Получить семена для текущего месяца"""
        if month == 3:
            results = []
            for category in ['томат', 'перец', 'баклажан']:
                seeds = seeds_db.get_seeds_by_category(category)[:3]
                results.extend(seeds)
            return results[:6]
        elif month == 4:
            results = []
            for category in ['капуста белокочанная', 'редис', 'петрушка']:
                seeds = seeds_db.get_seeds_by_category(category)[:2]
                results.extend(seeds)
            return results[:6]
        elif month == 5:
            results = []
            for category in ['томат', 'перец', 'огурец', 'кабачок']:
                seeds = seeds_db.get_seeds_by_category(category)[:2]
                results.extend(seeds)
            return results[:6]
        elif month in [6, 7]:
            return seeds_db.get_seeds_by_category('редис')[:3]
        elif month == 8:
            results = []
            for category in ['редис', 'петрушка']:
                seeds = seeds_db.get_seeds_by_category(category)[:2]
                results.extend(seeds)
            return results[:4]
        return []

    def needs_ai_consultation(self, message: str) -> bool:
        """
        Определить: нужен ли ИИ для ответа?
        
        ИИ нужен если:
        - Вопрос сложный, требует объяснения
        - Нет готового ответа в базе
        - Вопрос не о семенах из каталога
        """
        message_lower = message.lower()
        
        # Короткие вопросы без контекста — скорее всего простые
        if len(message_lower.split()) <= 3:
            is_simple, _ = self.is_simple_question(message)
            if is_simple:
                return False
        
        # Вопросы "как", "почему", "какой лучше" — требуют ИИ
        ai_indicators = [
            'как правильно', 'как лучше', 'почему', 'какой выбрать',
            'в чём разница', 'чем отличается', 'что лучше',
            'помоги выбрать', 'посоветуй', 'рекомендуй',
            'какой сорт', 'какие семена', 'какой гибрид',
            'когда лучше', 'где лучше', 'как вырастить',
            'как ухаживать', 'как бороться', 'как лечить',
            'что делать если', 'почему желтеют', 'почему не растёт'
        ]
        
        for indicator in ai_indicators:
            if indicator in message_lower:
                logger.debug(f"Требуется ИИ: найден индикатор '{indicator}'")
                return True
        
        # Длинные вопросы с деталями — требуют ИИ
        if len(message_lower.split()) > 5:
            return True
        
        return False

    async def get_response(
        self,
        message: str,
        ai_service=None,
        dialog_context: List[Dict[str, str]] = None
    ) -> Tuple[str, str]:
        """
        Главный метод: получить ответ на вопрос
        
        Возвращает: (ответ, источник)
        Источник: 'simple', 'seeds_db', 'ai'
        """
        message = message.strip()
        
        # 1. Проверка на запрос о покупке
        if self.is_purchase_request(message):
            logger.info("Запрос о покупке — отвечаем из базы")
            return self.get_purchase_info(message), 'purchase_info'
        
        # 2. Проверка на простой вопрос
        is_simple, category = self.is_simple_question(message)
        if is_simple:
            answer = self.get_simple_answer(category)
            if answer:
                logger.info(f"Простой вопрос ({category}) — отвечаем из шаблона")
                return answer, 'simple'
        
        # 3. Проверка на вопрос о семенах
        is_seed, seed_category = self.is_seed_question(message)
        if is_seed:
            recommendations = self.get_seed_recommendations(message, seed_category)
            if recommendations:
                logger.info(f"Вопрос о семенах ({seed_category}) — отвечаем из БД")
                return recommendations, 'seeds_db'
        
        # 4. Определяем: нужен ли ИИ?
        if not self.needs_ai_consultation(message):
            # Вопрос простой, но не нашли ответа — даём общий совет
            logger.info("Вопрос без ИИ — даём общий совет")
            return (
                " **Agrio рекомендует:**\n\n"
                "Для точного ответа уточните вопрос:\n"
                "• Какую культуру вы имеете в виду?\n"
                "• Какой у вас регион?\n"
                "• Что именно вас интересует?\n\n"
                "💡 Или спросите про конкретный сорт: `/seed [название]`"
            ), 'fallback'
        
        # 5. Требуется ИИ
        if ai_service:
            logger.info("Сложный вопрос — отправляем в YandexGPT")
            ai_answer = await ai_service.get_consultation(message, dialog_context)
            return ai_answer, 'ai'
        
        # ИИ недоступен
        logger.warning("Требуется ИИ, но сервис не подключён")
        return (
            "⚠️ **Извините, для ответа нужен ИИ-консультант.**\n\n"
            "Попробуйте:\n"
            "• Задать вопрос проще\n"
            "• Использовать команду `/seed [название]`\n"
            "• Посетить сайт: agrio.by"
        ), 'ai_unavailable'
