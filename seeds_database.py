"""
База данных семян магазина AGRIO.by
Содержит полную информацию о сортах и гибридах с рекомендациями
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class SeedVariety:
    """Класс для представления сорта/гибрида семян"""
    name: str
    category: str  # томаты, перец, морковь и т.д.
    variety_type: str  # гибрид F1 или сорт
    description: str = ""
    ripening_period: str = ""  # ультраранний, ранний, среднеранний, средний, поздний
    fruit_weight: str = ""  # масса плода
    features: List[str] = None
    growing_conditions: str = ""  # теплица, открытый грунт
    purpose: str = ""  # свежее потребление, переработка, рынок
    yield_level: str = ""  # высокая, средняя
    disease_resistance: str = ""
    additional_info: str = ""

    def __post_init__(self):
        if self.features is None:
            self.features = []

    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return asdict(self)


class SeedsDatabase:
    """База данных семян AGRIO"""

    def __init__(self):
        self.seeds: List[SeedVariety] = []
        self._init_database()

    def _init_database(self):
        """Инициализация базы данных семенами"""

        # ==================== ТОМАТЫ ====================
        tomatoes = [
            SeedVariety(
                name="СУПЕРНОВА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Ультраранний крупноплодный гибрид с превосходным вкусом",
                ripening_period="ультраранний (57-60 дней после пересадки)",
                fruit_weight="220-260 г",
                features=[
                    "Один из самых ранних крупноплодных томатов",
                    "Выровненные однородные плоды",
                    "Отличная лёжкость и транспортабельность",
                    "Превосходный вкус",
                    "Устойчивость к стрессовым условиям"
                ],
                growing_conditions="теплицы и открытый грунт",
                purpose="свежее потребление, переработка, коммерческое производство",
                yield_level="высокая, стабильная",
                disease_resistance="устойчив к основным заболеваниям",
                additional_info="Идеален для фермеров и производителей, работающих на рынок"
            ),
            SeedVariety(
                name="МАДРИД F1",
                category="томат",
                variety_type="гибрид F1",
                description="Крупноплодный би-колорный гибрид с уникальной окраской",
                ripening_period="среднеранний",
                fruit_weight="350-400 г (отдельные до 700 г)",
                features=[
                    "Уникальная лимонно-жёлтая окраска с красными переливами",
                    "Сердцевидная слегка вытянутая форма",
                    "Мясистая многокамерная мякоть",
                    "Сладкий нежный вкус с томатным ароматом",
                    "Высокая устойчивость к фитофторозу"
                ],
                growing_conditions="защищённый грунт (теплицы), пригоден для двух оборотов",
                purpose="свежий рынок, премиум-сегмент, салаты",
                yield_level="высокая стабильная",
                disease_resistance="к основным заболеваниям, включая фитофтороз",
                additional_info="Идеальный выбор для свежего рынка и премиум-сегмента"
            ),
            SeedVariety(
                name="САРРА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Надёжный гибрид для теплиц и открытого грунта",
                ripening_period="ранний",
                fruit_weight="180-220 г",
                features=["Выровненные плоды", "Хорошая транспортабельность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ОЛИВЕНЗА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Урожайный гибрид с отличными товарными качествами",
                ripening_period="среднеранний",
                fruit_weight="200-240 г",
                features=["Однородные плоды", "Длительное плодоношение"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КАНОВА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Качественный гибрид для коммерческого выращивания",
                ripening_period="среднеранний",
                fruit_weight="220-260 г",
                features=["Отличная лёжкость", "Товарный вид"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КОНГО F1",
                category="томат",
                variety_type="гибрид F1",
                description="Урожайный гибрид с выровненными плодами",
                ripening_period="средний",
                fruit_weight="200-230 г",
                features=["Выровненные плоды", "Устойчивость к болезням"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЧИМГАН F1",
                category="томат",
                variety_type="гибрид F1",
                description="Надёжный гибрид для различных условий выращивания",
                ripening_period="среднеранний",
                fruit_weight="190-220 г",
                features=["Адаптивность", "Стабильная урожайность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="АЙДАР F1",
                category="томат",
                variety_type="гибрид F1",
                description="Перспективный гибрид с отличными характеристиками",
                ripening_period="средний",
                fruit_weight="210-250 г",
                features=["Крупные плоды", "Хорошая транспортабельность"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="МАКАН F1",
                category="томат",
                variety_type="гибрид F1",
                description="Урожайный гибрид для теплиц",
                ripening_period="среднеранний",
                fruit_weight="200-230 г",
                features=["Стабильное плодоношение", "Выровненные плоды"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КАФА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Качественный тепличный гибрид",
                ripening_period="средний",
                fruit_weight="190-220 г",
                features=["Однородность плодов", "Устойчивость"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ФЕНДА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Надёжный гибрид с отличной урожайностью",
                ripening_period="среднеранний",
                fruit_weight="200-240 г",
                features=["Длительное хранение", "Транспортабельность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="РАВАН F1",
                category="томат",
                variety_type="гибрид F1",
                description="Перспективный гибрид для коммерческого выращивания",
                ripening_period="средний",
                fruit_weight="210-250 г",
                features=["Выровненные плоды", "Устойчивость к болезням"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПИНК КРИСТАЛ F1",
                category="томат",
                variety_type="гибрид F1",
                description="Розовоплодный гибрид с отличным вкусом",
                ripening_period="среднеранний",
                fruit_weight="220-260 г",
                features=["Розовые плоды", "Превосходный вкус", "Мясистая мякоть"],
                growing_conditions="теплицы",
                purpose="свежее потребление, премиум-сегмент",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ТУКАНО F1",
                category="томат",
                variety_type="гибрид F1",
                description="Урожайный гибрид для теплиц",
                ripening_period="среднеранний",
                fruit_weight="200-230 г",
                features=["Стабильная урожайность", "Выровненные плоды"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="РИХАМ F1",
                category="томат",
                variety_type="гибрид F1",
                description="Качественный гибрид с отличными товарными качествами",
                ripening_period="средний",
                fruit_weight="190-220 г",
                features=["Однородность", "Транспортабельность"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЦЕЛЕСТИН F1",
                category="томат",
                variety_type="гибрид F1",
                description="Надёжный тепличный гибрид",
                ripening_period="среднеранний",
                fruit_weight="200-240 г",
                features=["Стабильное плодоношение", "Устойчивость"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПЬЕТРАРОССА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Урожайный гибрид для открытого грунта и теплиц",
                ripening_period="средний",
                fruit_weight="180-220 г",
                features=["Сливовидная форма", "Отличная лёжкость"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЛУИДЖИ F1",
                category="томат",
                variety_type="гибрид F1",
                description="Качественный гибрид для коммерческого выращивания",
                ripening_period="среднеранний",
                fruit_weight="210-250 г",
                features=["Крупные плоды", "Выровненность"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="БАСТА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Универсальный гибрид для различных условий",
                ripening_period="среднеранний",
                fruit_weight="190-220 г",
                features=["Адаптивность", "Стабильная урожайность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КОЛИБРИ F1",
                category="томат",
                variety_type="гибрид F1",
                description="Перспективный гибрид с отличными характеристиками",
                ripening_period="ранний",
                fruit_weight="180-210 г",
                features=["Раннее созревание", "Выровненные плоды"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="АКЕЛА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Надёжный гибрид для теплиц и открытого грунта",
                ripening_period="среднеранний",
                fruit_weight="200-230 г",
                features=["Устойчивость к болезням", "Стабильность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПАНАМЕРА F1",
                category="томат",
                variety_type="гибрид F1",
                description="Качественный крупноплодный гибрид",
                ripening_period="средний",
                fruit_weight="230-280 г",
                features=["Крупные плоды", "Отличный вкус"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КРИСТАЛ F1",
                category="томат",
                variety_type="гибрид F1",
                description="Урожайный гибрид с выровненными плодами",
                ripening_period="среднеранний",
                fruit_weight="200-240 г",
                features=["Однородность", "Транспортабельность"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="АФЕН F1",
                category="томат",
                variety_type="гибрид F1",
                description="Перспективный гибрид для теплиц",
                ripening_period="средний",
                fruit_weight="210-250 г",
                features=["Стабильное плодоношение", "Устойчивость"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="РЕДКАН F1",
                category="томат",
                variety_type="гибрид F1",
                description="Урожайный гибрид с отличными товарными качествами",
                ripening_period="среднеранний",
                fruit_weight="190-220 г",
                features=["Выровненные плоды", "Лёжкость"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ДРАЙВЕР F1",
                category="томат",
                variety_type="гибрид F1",
                description="Надёжный гибрид для коммерческого выращивания",
                ripening_period="среднеранний",
                fruit_weight="200-240 г",
                features=["Стабильная урожайность", "Устойчивость"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ВИСКОНТ F1",
                category="томат",
                variety_type="гибрид F1",
                description="Качественный гибрид с отличной урожайностью",
                ripening_period="средний",
                fruit_weight="210-250 г",
                features=["Крупные плоды", "Транспортабельность"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПАТЗИ F1",
                category="томат",
                variety_type="гибрид F1",
                description="Универсальный гибрид для различных условий",
                ripening_period="среднеранний",
                fruit_weight="190-220 г",
                features=["Адаптивность", "Стабильность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="МИНОПРИО F1",
                category="томат",
                variety_type="гибрид F1",
                description="Перспективный гибрид с отличными характеристиками",
                ripening_period="средний",
                fruit_weight="200-240 г",
                features=["Выровненные плоды", "Устойчивость к болезням"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(tomatoes)

        # ==================== ПЕРЕЦ ====================
        peppers = [
            SeedVariety(
                name="ГЕРКУЛЕС F1",
                category="перец",
                variety_type="гибрид F1",
                description="Лидер среди перцев для переработки с кубовидными плодами",
                ripening_period="среднеранний",
                fruit_weight="220-250 г (до 300 г)",
                features=[
                    "Классическая кубовидная 4-камерная форма",
                    "Толщина стенки 7-10 мм (до 1 см)",
                    "Очень сладкий вкус в зелёной и красной стадии",
                    "Отличная транспортабельность и лёжкость",
                    "Компактное растение с высоким урожаем"
                ],
                growing_conditions="теплицы, открытый грунт",
                purpose="переработка, заморозка, свежий рынок, оптовые поставки",
                yield_level="высокоурожайный",
                disease_resistance="устойчив к основным болезням культуры",
                additional_info="Рекомендуется для фермерских хозяйств и оптовых производителей"
            ),
            SeedVariety(
                name="РЕД ДЖЕВЕЛ F1",
                category="перец",
                variety_type="гибрид F1",
                description="Красный кубовидный перец премиум класса",
                ripening_period="среднеранний",
                fruit_weight="200-240 г",
                features=["Красивая красная окраска", "Кубовидная форма", "Премиум качество"],
                growing_conditions="теплицы",
                purpose="свежий рынок, премиум-сегмент",
                yield_level="высокая"
            ),
            SeedVariety(
                name="АМАРОК F1",
                category="перец",
                variety_type="гибрид F1",
                description="Урожайный гибрид сладкого перца",
                ripening_period="среднеранний",
                fruit_weight="180-220 г",
                features=["Выровненные плоды", "Устойчивость к болезням"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЧЕВИ F1",
                category="перец",
                variety_type="гибрид F1",
                description="Качественный гибрид для теплиц",
                ripening_period="средний",
                fruit_weight="190-230 г",
                features=["Однородные плоды", "Хорошая транспортабельность"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ВАНГАРД F1",
                category="перец",
                variety_type="гибрид F1",
                description="Ранний урожайный гибрид",
                ripening_period="ранний",
                fruit_weight="170-200 г",
                features=["Раннее созревание", "Стабильная урожайность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="РЕДКАН F1",
                category="перец",
                variety_type="гибрид F1",
                description="Универсальный гибрид с отличными характеристиками",
                ripening_period="среднеранний",
                fruit_weight="180-220 г",
                features=["Адаптивность", "Устойчивость"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КАРИСМА F1",
                category="перец",
                variety_type="гибрид F1",
                description="Качественный гибрид для коммерческого выращивания",
                ripening_period="средний",
                fruit_weight="200-240 г",
                features=["Крупные плоды", "Товарный вид"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СПРИНГБОКС F1",
                category="перец",
                variety_type="гибрид F1",
                description="Надёжный гибрид для теплиц",
                ripening_period="среднеранний",
                fruit_weight="190-220 г",
                features=["Стабильное плодоношение", "Выровненные плоды"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ФЛАМИНГО F1",
                category="перец",
                variety_type="гибрид F1",
                description="Перспективный гибрид с розовыми плодами",
                ripening_period="средний",
                fruit_weight="180-210 г",
                features=["Розовая окраска", "Отличный вкус"],
                growing_conditions="теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЯСНА F1",
                category="перец",
                variety_type="гибрид F1",
                description="Урожайный гибрид для теплиц и открытого грунта",
                ripening_period="среднеранний",
                fruit_weight="170-200 г",
                features=["Устойчивость", "Стабильная урожайность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ГОМЕС F1",
                category="перец",
                variety_type="гибрид F1",
                description="Качественный гибрид с выровненными плодами",
                ripening_period="средний",
                fruit_weight="190-230 г",
                features=["Однородность", "Транспортабельность"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЛИМОН",
                category="перец",
                variety_type="сорт",
                description="Сорт сладкого перца с жёлтой окраской",
                ripening_period="средний",
                fruit_weight="150-180 г",
                features=["Жёлтая окраска", "Сладкий вкус"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="средняя"
            ),
            SeedVariety(
                name="ХУРМА",
                category="перец",
                variety_type="сорт",
                description="Сорт сладкого перца с оранжевой окраской",
                ripening_period="средний",
                fruit_weight="160-190 г",
                features=["Оранжевая окраска", "Сладкий вкус"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление",
                yield_level="средняя"
            ),
        ]
        self.seeds.extend(peppers)

        # ==================== МОРКОВЬ ====================
        carrots = [
            SeedVariety(
                name="БОЛИВАР F1",
                category="морковь",
                variety_type="гибрид F1",
                description="Раннеспелый высокоурожайный гибрид моркови",
                ripening_period="раннеспелый",
                fruit_weight="150-200 г",
                features=["Раннее созревание", "Выровненные корнеплоды", "Отличный вкус"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка, хранение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПОЛИДОР F1",
                category="морковь",
                variety_type="гибрид F1",
                description="Урожайный гибрид моркови с выровненными корнеплодами",
                ripening_period="среднеранний",
                fruit_weight="140-180 г",
                features=["Однородные корнеплоды", "Хорошая лёжкость"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, хранение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="САНТОРИН F1",
                category="морковь",
                variety_type="гибрид F1",
                description="Качественный гибрид для коммерческого выращивания",
                ripening_period="средний",
                fruit_weight="150-190 г",
                features=["Выровненные корнеплоды", "Товарный вид"],
                growing_conditions="открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПАТЗИ F1",
                category="морковь",
                variety_type="гибрид F1",
                description="Универсальный гибрид моркови",
                ripening_period="среднеранний",
                fruit_weight="140-170 г",
                features=["Адаптивность", "Стабильная урожайность"],
                growing_conditions="открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КАЗИМИР F1",
                category="морковь",
                variety_type="гибрид F1",
                description="Надёжный гибрид для открытого грунта",
                ripening_period="средний",
                fruit_weight="150-180 г",
                features=["Устойчивость к болезням", "Хорошее хранение"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, хранение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КРОКЕТ",
                category="морковь",
                variety_type="сорт",
                description="Сорт моркови с отличными вкусовыми качествами",
                ripening_period="средний",
                fruit_weight="130-160 г",
                features=["Сладкий вкус", "Выровненные корнеплоды"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, детское питание",
                yield_level="средняя"
            ),
            SeedVariety(
                name="АРДЕНТ F1",
                category="морковь",
                variety_type="гибрид F1",
                description="Перспективный гибрид моркови",
                ripening_period="среднеранний",
                fruit_weight="140-170 г",
                features=["Устойчивость", "Стабильная урожайность"],
                growing_conditions="открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(carrots)

        # ==================== КАПУСТА БЕЛОКОЧАННАЯ ====================
        cabbages = [
            SeedVariety(
                name="ЦЕНТУРИОН F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Урожайный гибрид белокочанной капусты",
                ripening_period="среднепоздний",
                fruit_weight="3-4 кг",
                features=["Плотные кочаны", "Хорошая лёжкость"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, хранение, квашение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ГИГАНТ F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Крупноплодный гибрид капусты",
                ripening_period="средний",
                fruit_weight="4-6 кг",
                features=["Крупные кочаны", "Высокая урожайность"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="РАНОКИ F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Раннеспелый гибрид капусты",
                ripening_period="раннеспелый",
                fruit_weight="2-3 кг",
                features=["Раннее созревание", "Нежный вкус"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СИР F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Качественный гибрид для коммерческого выращивания",
                ripening_period="средний",
                fruit_weight="3-4 кг",
                features=["Выровненные кочаны", "Товарный вид"],
                growing_conditions="открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ВИСКОНТ F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Надёжный гибрид с отличной урожайностью",
                ripening_period="среднепоздний",
                fruit_weight="3-5 кг",
                features=["Плотные кочаны", "Длительное хранение"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, хранение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="БРИГАДИР F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Урожайный гибрид для открытого грунта",
                ripening_period="средний",
                fruit_weight="3-4 кг",
                features=["Устойчивость к болезням", "Стабильная урожайность"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, квашение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КАУНТ F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Качественный гибрид капусты",
                ripening_period="среднеранний",
                fruit_weight="2-3 кг",
                features=["Выровненные кочаны", "Хороший вкус"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="БРАВО F1",
                category="капуста белокочанная",
                variety_type="гибрид F1",
                description="Перспективный гибрид с отличными характеристиками",
                ripening_period="средний",
                fruit_weight="3-4 кг",
                features=["Устойчивость", "Товарный вид"],
                growing_conditions="открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(cabbages)

        # ==================== АРБУЗ ====================
        watermelons = [
            SeedVariety(
                name="ЛИВИЯ F1",
                category="арбуз",
                variety_type="гибрид F1",
                description="Раннеспелый высокопродуктивный гибрид арбуза",
                ripening_period="раннеспелый",
                fruit_weight="8-12 кг",
                features=["Насыщенно-красная хрустящая мякоть", "Ароматный", "Раннее созревание"],
                growing_conditions="теплицы, открытый грунт (южные регионы)",
                purpose="свежее потребление",
                yield_level="высокопродуктивный",
                additional_info="Отлично адаптирован к климатическим условиям Беларуси"
            ),
            SeedVariety(
                name="ЭПИКА F1",
                category="арбуз",
                variety_type="гибрид F1",
                description="Урожайный гибрид арбуза с отличными вкусовыми качествами",
                ripening_period="раннеспелый",
                fruit_weight="7-10 кг",
                features=["Сладкая мякоть", "Тонкая корка", "Устойчивость к болезням"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЦЕЛИН F1",
                category="арбуз",
                variety_type="гибрид F1",
                description="Качественный гибрид арбуза",
                ripening_period="среднеранний",
                fruit_weight="8-11 кг",
                features=["Выровненные плоды", "Хорошая транспортабельность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СУПЕР ДОНИЯ F1",
                category="арбуз",
                variety_type="гибрид F1",
                description="Ультраранний гибрид арбуза",
                ripening_period="ультраранний",
                fruit_weight="6-9 кг",
                features=["Очень раннее созревание", "Сладкая мякоть"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СИР F1",
                category="арбуз",
                variety_type="гибрид F1",
                description="Надёжный гибрид арбуза",
                ripening_period="среднеранний",
                fruit_weight="7-10 кг",
                features=["Стабильная урожайность", "Устойчивость"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ВИСКОНТ F1",
                category="арбуз",
                variety_type="гибрид F1",
                description="Крупноплодный гибрид арбуза",
                ripening_period="средний",
                fruit_weight="10-14 кг",
                features=["Крупные плоды", "Отличный вкус"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КАПРИЗ",
                category="арбуз",
                variety_type="сорт",
                description="Сорт арбуза с отличными вкусовыми качествами",
                ripening_period="средний",
                fruit_weight="6-8 кг",
                features=["Сладкая мякоть", "Ароматный"],
                growing_conditions="открытый грунт (южные регионы)",
                purpose="свежее потребление",
                yield_level="средняя"
            ),
        ]
        self.seeds.extend(watermelons)

        # ==================== КАБАЧОК ====================
        zucchinis = [
            SeedVariety(
                name="ЯСНА F1",
                category="кабачок",
                variety_type="гибрид F1",
                description="Урожайный гибрид кабачка",
                ripening_period="раннеспелый",
                fruit_weight="0.8-1.2 кг",
                features=["Раннее созревание", "Выровненные плоды"],
                growing_conditions="открытый грунт, теплицы",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СУПЕР ДОНИЯ F1",
                category="кабачок",
                variety_type="гибрид F1",
                description="Раннеспелый высокоурожайный гибрид",
                ripening_period="раннеспелый",
                fruit_weight="0.9-1.3 кг",
                features=["Высокая урожайность", "Длительное плодоношение"],
                growing_conditions="открытый грунт, теплицы",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="АСМА F1",
                category="кабачок",
                variety_type="гибрид F1",
                description="Качественный гибрид кабачка",
                ripening_period="среднеранний",
                fruit_weight="0.8-1.1 кг",
                features=["Выровненные плоды", "Хорошая транспортабельность"],
                growing_conditions="открытый грунт, теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЛИВИЯ F1",
                category="кабачок",
                variety_type="гибрид F1",
                description="Урожайный гибрид с отличными характеристиками",
                ripening_period="раннеспелый",
                fruit_weight="0.9-1.2 кг",
                features=["Раннее созревание", "Нежная мякоть"],
                growing_conditions="открытый грунт, теплицы",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КОНГО F1",
                category="кабачок",
                variety_type="гибрид F1",
                description="Надёжный гибрид кабачка",
                ripening_period="среднеранний",
                fruit_weight="0.8-1.1 кг",
                features=["Стабильная урожайность", "Устойчивость"],
                growing_conditions="открытый грунт, теплицы",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПОЛИДОР F1",
                category="кабачок",
                variety_type="гибрид F1",
                description="Качественный гибрид для коммерческого выращивания",
                ripening_period="среднеранний",
                fruit_weight="0.7-1 кг",
                features=["Выровненные плоды", "Товарный вид"],
                growing_conditions="открытый грунт, теплицы",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЦЕЛЕСТИН F1",
                category="кабачок",
                variety_type="гибрид F1",
                description="Перспективный гибрид кабачка",
                ripening_period="среднеранний",
                fruit_weight="0.8-1.1 кг",
                features=["Стабильное плодоношение", "Устойчивость к болезням"],
                growing_conditions="открытый грунт, теплицы",
                purpose="универсальное",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(zucchinis)

        # ==================== ТЫКВА ====================
        pumpkins = [
            SeedVariety(
                name="ГЛАДИАТОР F1",
                category="тыква",
                variety_type="гибрид F1",
                description="Урожайный гибрид тыквы",
                ripening_period="среднеспелый",
                fruit_weight="4-6 кг",
                features=["Выровненные плоды", "Сладкая мякоть"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СПИТФАЕР F1",
                category="тыква",
                variety_type="гибрид F1",
                description="Качественный гибрид тыквы",
                ripening_period="среднеспелый",
                fruit_weight="3-5 кг",
                features=["Хорошая лёжкость", "Отличный вкус"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, хранение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СИБЕЛЬ F1",
                category="тыква",
                variety_type="гибрид F1",
                description="Урожайный гибрид для открытого грунта",
                ripening_period="среднеспелый",
                fruit_weight="4-6 кг",
                features=["Устойчивость к болезням", "Стабильная урожайность"],
                growing_conditions="открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="РУЖ ВИФ ДЕ ТАМП",
                category="тыква",
                variety_type="сорт",
                description="Традиционный французский сорт мускатной тыквы",
                ripening_period="среднепоздний",
                fruit_weight="5-8 кг",
                features=["Мускатный аромат", "Сладкая мякоть", "Традиционный сорт"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка, десерты",
                yield_level="средняя"
            ),
            SeedVariety(
                name="ГОМЕС F1",
                category="тыква",
                variety_type="гибрид F1",
                description="Надёжный гибрид тыквы",
                ripening_period="среднеспелый",
                fruit_weight="4-6 кг",
                features=["Стабильная урожайность", "Хорошее хранение"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, хранение",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КРАНЧИК F1",
                category="тыква",
                variety_type="гибрид F1",
                description="Перспективный гибрид тыквы",
                ripening_period="среднеспелый",
                fruit_weight="3-5 кг",
                features=["Выровненные плоды", "Устойчивость"],
                growing_conditions="открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="МУСКАТ ДЕ ПРОВАНС",
                category="тыква",
                variety_type="сорт",
                description="Классический французский сорт мускатной тыквы",
                ripening_period="среднепоздний",
                fruit_weight="6-10 кг",
                features=["Мускатный аромат", "Очень сладкая мякоть", "Плоско-округлая форма"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, десерты, переработка",
                yield_level="средняя"
            ),
        ]
        self.seeds.extend(pumpkins)

        # ==================== БРОККОЛИ ====================
        broccolis = [
            SeedVariety(
                name="ВАВИЛОН F1",
                category="брокколи",
                variety_type="гибрид F1",
                description="Урожайный гибрид брокколи",
                ripening_period="среднеранний",
                fruit_weight="500-800 г",
                features=["Плотные головки", "Хорошее отрастание боковых побегов"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КОРОС F1",
                category="брокколи",
                variety_type="гибрид F1",
                description="Раннеспелый гибрид брокколи",
                ripening_period="раннеспелый",
                fruit_weight="400-600 г",
                features=["Раннее созревание", "Выровненные головки"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СИГНО F1",
                category="брокколи",
                variety_type="гибрид F1",
                description="Качественный гибрид брокколи",
                ripening_period="среднеранний",
                fruit_weight="500-700 г",
                features=["Плотные соцветия", "Хорошая транспортабельность"],
                growing_conditions="открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ФЕНДА F1",
                category="брокколи",
                variety_type="гибрид F1",
                description="Надёжный гибрид брокколи",
                ripening_period="средний",
                fruit_weight="500-800 г",
                features=["Стабильная урожайность", "Устойчивость к болезням"],
                growing_conditions="открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ДЮРОК F1",
                category="брокколи",
                variety_type="гибрид F1",
                description="Урожайный гибрид для открытого грунта",
                ripening_period="среднеспелый",
                fruit_weight="600-900 г",
                features=["Крупные головки", "Длительное плодоношение"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ФАБИНА F1",
                category="брокколи",
                variety_type="гибрид F1",
                description="Раннеспелый высокоурожайный гибрид",
                ripening_period="раннеспелый",
                fruit_weight="400-600 г",
                features=["Раннее созревание", "Хорошее ветвление"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СПИТФАЕР F1",
                category="брокколи",
                variety_type="гибрид F1",
                description="Качественный гибрид брокколи",
                ripening_period="среднеранний",
                fruit_weight="500-700 г",
                features=["Выровненные головки", "Устойчивость"],
                growing_conditions="открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(broccolis)

        # ==================== ДЫНЯ ====================
        melons = [
            SeedVariety(
                name="МАОРИ F1",
                category="дыня",
                variety_type="гибрид F1",
                description="Раннеспелый гибрид дыни",
                ripening_period="раннеспелый",
                fruit_weight="1.5-2 кг",
                features=["Раннее созревание", "Сладкая ароматная мякоть"],
                growing_conditions="теплицы, открытый грунт (южные регионы)",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="МАЗИН F1",
                category="дыня",
                variety_type="гибрид F1",
                description="Урожайный гибрид дыни",
                ripening_period="среднеранний",
                fruit_weight="2-3 кг",
                features=["Выровненные плоды", "Отличный вкус"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="МАБЕЛЛА F1",
                category="дыня",
                variety_type="гибрид F1",
                description="Качественный гибрид дыни",
                ripening_period="раннеспелый",
                fruit_weight="1.5-2.5 кг",
                features=["Раннее созревание", "Ароматная мякоть"],
                growing_conditions="теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ПАТЗИ F1",
                category="дыня",
                variety_type="гибрид F1",
                description="Универсальный гибрид дыни",
                ripening_period="среднеранний",
                fruit_weight="2-2.5 кг",
                features=["Адаптивность", "Стабильная урожайность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="универсальное",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ДРАЙВЕР F1",
                category="дыня",
                variety_type="гибрид F1",
                description="Надёжный гибрид дыни",
                ripening_period="среднеранний",
                fruit_weight="2-3 кг",
                features=["Устойчивость к болезням", "Хорошая транспортабельность"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
            SeedVariety(
                name="САБОРД F1",
                category="дыня",
                variety_type="гибрид F1",
                description="Урожайный гибрид дыни",
                ripening_period="среднеспелый",
                fruit_weight="2.5-3.5 кг",
                features=["Крупные плоды", "Сладкая мякоть"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
            SeedVariety(
                name="МЕГАТОН F1",
                category="дыня",
                variety_type="гибрид F1",
                description="Крупноплодный гибрид дыни",
                ripening_period="среднеспелый",
                fruit_weight="3-5 кг",
                features=["Очень крупные плоды", "Отличный вкус"],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(melons)

        # ==================== БАКЛАЖАН ====================
        eggplants = [
            SeedVariety(
                name="ФАБИНА F1",
                category="баклажан",
                variety_type="гибрид F1",
                description="Раннеспелый гибрид баклажана с высокой товарностью",
                ripening_period="раннеспелый (60-65 дней)",
                fruit_weight="150-200 г",
                features=[
                    "Формирует одновременно 6-8 плодов",
                    "Концентрированный урожай",
                    "Высокая товарность",
                    "Отличный вкус"
                ],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая",
                disease_resistance="устойчив к основным заболеваниям"
            ),
            SeedVariety(
                name="ЭПИК F1",
                category="баклажан",
                variety_type="гибрид F1",
                description="Высокоурожайный раннеспелый гибрид баклажана",
                ripening_period="раннеспелый (64 дня после высадки)",
                fruit_weight="200-250 г",
                features=[
                    "Высокая урожайность",
                    "Выровненные плоды",
                    "Отличный вкус",
                    "Хорошая транспортабельность"
                ],
                growing_conditions="теплицы, открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая",
                disease_resistance="устойчив к вирусным заболеваниям"
            ),
            SeedVariety(
                name="МИРВАЛ F1",
                category="баклажан",
                variety_type="гибрид F1",
                description="Качественный гибрид баклажана",
                ripening_period="среднеранний",
                fruit_weight="180-230 г",
                features=["Выровненные плоды", "Стабильная урожайность"],
                growing_conditions="теплицы",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(eggplants)

        # ==================== КУКУРУЗА САХАРНАЯ ====================
        corn = [
            SeedVariety(
                name="ЛАКОМКА F1",
                category="кукуруза сахарная",
                variety_type="гибрид F1",
                description="Раннеспелый гибрид сахарной кукурузы",
                ripening_period="раннеспелый (70-75 дней)",
                fruit_weight="початок 180-200 г",
                features=["Сладкие зёрна", "Нежная мякоть", "Раннее созревание"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, консервирование",
                yield_level="высокая"
            ),
            SeedVariety(
                name="СПИРИТ F1",
                category="кукуруза сахарная",
                variety_type="гибрид F1",
                description="Ультраранний гибрид сахарной кукурузы",
                ripening_period="ультраранний (65-68 дней)",
                fruit_weight="початок 200-250 г",
                features=["Очень сладкие зёрна", "Нежная оболочка", "Устойчивость к болезням"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, консервирование",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(corn)

        # ==================== ЦВЕТНАЯ КАПУСТА ====================
        cauliflower = [
            SeedVariety(
                name="ФАРИДО F1",
                category="цветная капуста",
                variety_type="гибрид F1",
                description="Урожайный гибрид цветной капусты",
                ripening_period="среднеранний",
                fruit_weight="800-1200 г",
                features=["Плотные белые головки", "Хорошее покрытие листьями"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
            SeedVariety(
                name="КОРИНДО F1",
                category="цветная капуста",
                variety_type="гибрид F1",
                description="Качественный гибрид цветной капусты",
                ripening_period="средний",
                fruit_weight="900-1300 г",
                features=["Выровненные головки", "Устойчивость к болезням"],
                growing_conditions="открытый грунт",
                purpose="свежий рынок",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(cauliflower)

        # ==================== ПЕТРУШКА ====================
        parsley = [
            SeedVariety(
                name="ИТАЛЬЯНСКИЙ ГИГАНТ",
                category="петрушка",
                variety_type="сорт",
                description="Сорт листовой петрушки с крупными листьями",
                ripening_period="среднеспелый",
                fruit_weight="",
                features=["Крупные ароматные листья", "Высокая урожайность зелени"],
                growing_conditions="открытый грунт, теплицы",
                purpose="свежее потребление, переработка",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(parsley)

        # ==================== РЕДИС ====================
        radish = [
            SeedVariety(
                name="КРАСНЫЙ ВЕЛИКАН",
                category="редис",
                variety_type="сорт",
                description="Крупноплодный сорт редиса",
                ripening_period="среднеспелый",
                fruit_weight="80-100 г",
                features=["Крупные корнеплоды", "Сочная мякоть"],
                growing_conditions="открытый грунт, теплицы",
                purpose="свежее потребление",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(radish)

        # ==================== СВЕКЛА СТОЛОВАЯ ====================
        beet = [
            SeedVariety(
                name="ДЕТРОЙТ",
                category="свекла столовая",
                variety_type="сорт",
                description="Классический сорт столовой свеклы",
                ripening_period="среднеспелый",
                fruit_weight="200-300 г",
                features=["Выровненные корнеплоды", "Отличный вкус", "Хорошее хранение"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, переработка, хранение",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(beet)

        # ==================== СПАРЖЕВАЯ ФАСОЛЬ ====================
        beans = [
            SeedVariety(
                name="ФАВОРИТ F1",
                category="спаржевая фасоль",
                variety_type="гибрид F1",
                description="Урожайный гибрид спаржевой фасоли",
                ripening_period="среднеранний",
                fruit_weight="стручок 12-15 см",
                features=["Длинные стручки", "Отсутствие волокон", "Высокая урожайность"],
                growing_conditions="открытый грунт, теплицы",
                purpose="свежее потребление, заморозка, консервирование",
                yield_level="высокая"
            ),
            SeedVariety(
                name="ЗОЛОТАЯ КОРОЛЕВНА",
                category="спаржевая фасоль",
                variety_type="сорт",
                description="Сорт спаржевой фасоли с жёлтыми стручками",
                ripening_period="среднеспелый",
                fruit_weight="стручок 15-18 см",
                features=["Жёлтые стручки", "Нежный вкус", "Длительное плодоношение"],
                growing_conditions="открытый грунт",
                purpose="свежее потребление, консервирование",
                yield_level="высокая"
            ),
        ]
        self.seeds.extend(beans)

    def get_all_categories(self) -> List[str]:
        """Получить список всех категорий семян"""
        categories = set()
        for seed in self.seeds:
            categories.add(seed.category)
        return sorted(list(categories))

    def get_seeds_by_category(self, category: str) -> List[SeedVariety]:
        """Получить все семена из категории"""
        return [seed for seed in self.seeds if seed.category.lower() == category.lower()]

    def search_by_name(self, query: str) -> List[SeedVariety]:
        """Поиск семян по названию"""
        query_lower = query.lower()
        results = []
        for seed in self.seeds:
            if query_lower in seed.name.lower():
                results.append(seed)
        return results

    def get_seed_by_name(self, name: str) -> Optional[SeedVariety]:
        """Получить конкретный сорт по названию"""
        name_upper = name.upper()
        for seed in self.seeds:
            if seed.name.upper() == name_upper:
                return seed
        return None

    def search_by_features(self, keywords: List[str]) -> List[SeedVariety]:
        """Поиск семян по характеристикам"""
        results = []
        keywords_lower = [kw.lower() for kw in keywords]

        for seed in self.seeds:
            score = 0
            # Проверяем название
            for kw in keywords_lower:
                if kw in seed.name.lower():
                    score += 3
                if kw in seed.description.lower():
                    score += 2
                if kw in seed.category.lower():
                    score += 2
                # Проверяем характеристики
                for feature in seed.features:
                    if kw in feature.lower():
                        score += 1
                if kw in seed.ripening_period.lower():
                    score += 1
                if kw in seed.purpose.lower():
                    score += 1

            if score > 0:
                results.append((score, seed))

        # Сортируем по релевантности
        results.sort(key=lambda x: x[0], reverse=True)
        return [seed for score, seed in results]

    def get_recommendations_for_category(self, category: str, criteria: Dict) -> List[SeedVariety]:
        """
        Получить рекомендации по категории с учётом критериев

        Args:
            category: категория семян
            criteria: критерии выбора (ripening_period, purpose, growing_conditions и т.д.)
        """
        seeds = self.get_seeds_by_category(category)

        if not criteria:
            return seeds[:5]  # Возвращаем топ-5 по умолчанию

        scored_seeds = []
        for seed in seeds:
            score = 0

            # Проверяем сроки созревания
            if criteria.get('ripening_period'):
                if criteria['ripening_period'].lower() in seed.ripening_period.lower():
                    score += 5

            # Проверяем назначение
            if criteria.get('purpose'):
                if criteria['purpose'].lower() in seed.purpose.lower():
                    score += 3

            # Проверяем условия выращивания
            if criteria.get('growing_conditions'):
                if criteria['growing_conditions'].lower() in seed.growing_conditions.lower():
                    score += 3

            # Проверяем массу плода
            if criteria.get('fruit_weight'):
                if criteria['fruit_weight'].lower() in seed.fruit_weight.lower():
                    score += 2

            # Проверяем особенности
            if criteria.get('features'):
                for feature in criteria['features']:
                    if feature.lower() in seed.description.lower():
                        score += 2
                    for f in seed.features:
                        if feature.lower() in f.lower():
                            score += 1

            scored_seeds.append((score, seed))

        # Сортируем по релевантности
        scored_seeds.sort(key=lambda x: x[0], reverse=True)

        # Возвращаем топ-5
        return [seed for score, seed in scored_seeds[:5]]

    def format_seed_info(self, seed: SeedVariety) -> str:
        """Форматировать информацию о семени для вывода"""
        info = f"🌱 **{seed.name}** ({seed.variety_type})\n\n"
        info += f"**Категория:** {seed.category.capitalize()}\n"

        if seed.description:
            info += f"**Описание:** {seed.description}\n\n"

        if seed.ripening_period:
            info += f"📅 **Срок созревания:** {seed.ripening_period}\n"

        if seed.fruit_weight:
            info += f"⚖️ **Масса плода:** {seed.fruit_weight}\n"

        if seed.features:
            info += "\n**Особенности:**\n"
            for feature in seed.features[:5]:  # Максимум 5 особенностей
                info += f"• {feature}\n"

        if seed.growing_conditions:
            info += f"\n🏡 **Условия выращивания:** {seed.growing_conditions}\n"

        if seed.purpose:
            info += f"🎯 **Назначение:** {seed.purpose}\n"

        if seed.yield_level:
            info += f"📊 **Урожайность:** {seed.yield_level}\n"

        if seed.disease_resistance:
            info += f"🛡️ **Устойчивость:** {seed.disease_resistance}\n"

        if seed.additional_info:
            info += f"\n💡 **Дополнительно:** {seed.additional_info}\n"

        return info

    def get_catalog_summary(self) -> str:
        """Получить краткую сводку по всему каталогу"""
        categories = self.get_all_categories()

        summary = "🌱 **КАТАЛОГ СЕМЯН AGRIO.BY**\n\n"
        summary += f"Всего в каталоге: **{len(self.seeds)}** сортов и гибридов\n\n"

        for category in categories:
            count = len(self.get_seeds_by_category(category))
            emoji = self._get_category_emoji(category)
            summary += f"{emoji} **{category.capitalize()}** — {count} шт.\n"

        return summary

    def _get_category_emoji(self, category: str) -> str:
        """Получить эмодзи для категории"""
        emojis = {
            "томат": "🍅",
            "перец": "🌶️",
            "морковь": "🥕",
            "капуста белокочанная": "🥬",
            "арбуз": "🍉",
            "кабачок": "🥒",
            "тыква": "🎃",
            "брокколи": "🥦",
            "дыня": "🍈",
            "баклажан": "🍆",
            "кукуруза сахарная": "🌽",
            "цветная капуста": "🥦",
            "петрушка": "🌿",
            "редис": "🔴",
            "свекла столовая": "🟣",
            "спаржевая фасоль": "🫘",
        }
        return emojis.get(category.lower(), "🌱")


# Глобальный экземпляр базы данных
seeds_db = SeedsDatabase()
