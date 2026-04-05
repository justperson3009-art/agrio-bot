"""
База данных семян магазина AGRIO.by
Содержит полную информацию о сортах и гибридах с рекомендациями

Данные взяты с официального сайта agrio.by (93 сорта)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class SeedVariety:
    """Класс для представления сорта/гибрида семян"""
    name: str
    category: str
    variety_type: str = "гибрид F1"
    description: str = ""
    ripening_period: str = ""
    fruit_weight: str = ""
    features: List[str] = None
    growing_conditions: str = ""
    purpose: str = ""
    yield_level: str = ""
    disease_resistance: str = ""
    additional_info: str = ""

    def __post_init__(self):
        if self.features is None:
            self.features = []

    def to_dict(self) -> dict:
        return asdict(self)


class SeedsDatabase:
    """База данных семян AGRIO — 93 сорта с сайта agrio.by"""

    def __init__(self):
        self.seeds: List[SeedVariety] = []
        self._init_database()

    def _init_database(self):
        """Инициализация базы данных семенами с сайта AGRIO.by"""

        # ==================== ТОМАТ (25) ====================
        tomatoes = [
            SeedVariety(name="МИНОПРИО F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="МАДРИД F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="САРРА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ОЛИВЕНЗА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="КАНОВА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="КОНГО F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ЧИМГАН F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="АЙДАР F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="МАКАН F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="КАФА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ФЕНДА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="РАВАН F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ПИНК КРИСТАЛ F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ТУКАНО F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="РИХАН F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ЦЕЛЕСТИН F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ПЬЕТАРОССА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ЛУИДЖИ F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="СУПЕРНОВА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="БАСТА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="КОЛИБРИ F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="АКЕЛА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="ПАНАМЕРА F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="КРИСТАЛ F1", category="томат", variety_type="гибрид F1"),
            SeedVariety(name="АФЕН F1", category="томат", variety_type="гибрид F1"),
        ]
        self.seeds.extend(tomatoes)

        # ==================== ПЕРЕЦ (9) ====================
        peppers = [
            SeedVariety(name="АМАРОК F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="ЧЕВИ F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="РЕД ДЖЕВЕЛ F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="ВАНГАРД F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="РЕДКАН F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="ГЕРКУЛЕС F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="КАРИСМА F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="СПРИНГБОКС F1", category="перец", variety_type="гибрид F1"),
            SeedVariety(name="ФЛАМИНГО F1", category="перец", variety_type="гибрид F1"),
        ]
        self.seeds.extend(peppers)

        # ==================== МОРКОВЬ (4) ====================
        carrots = [
            SeedVariety(name="ПОЛИДОР F1", category="морковь", variety_type="гибрид F1"),
            SeedVariety(name="БОЛИВАР F1", category="морковь", variety_type="гибрид F1"),
            SeedVariety(name="САНТОРИН F1", category="морковь", variety_type="гибрид F1"),
            SeedVariety(name="ПАТЗИ F1", category="морковь", variety_type="гибрид F1"),
        ]
        self.seeds.extend(carrots)

        # ==================== КАПУСТА БЕЛОКОЧАННАЯ (8) ====================
        cabbage_white = [
            SeedVariety(name="ЦЕНТУРИОН F1", category="капуста белокочанная", variety_type="гибрид F1"),
            SeedVariety(name="ГИГАНТ F1", category="капуста белокочанная", variety_type="гибрид F1"),
            SeedVariety(name="РАНОККИ F1", category="капуста белокочанная", variety_type="гибрид F1"),
            SeedVariety(name="СИР F1", category="капуста белокочанная", variety_type="гибрид F1"),
            SeedVariety(name="ВИСКОНТ F1", category="капуста белокочанная", variety_type="гибрид F1"),
            SeedVariety(name="БРИГАДИР F1", category="капуста белокочанная", variety_type="гибрид F1"),
            SeedVariety(name="КАУНТ F1", category="капуста белокочанная", variety_type="гибрид F1"),
            SeedVariety(name="БРАВО F1", category="капуста белокочанная", variety_type="гибрид F1"),
        ]
        self.seeds.extend(cabbage_white)

        # ==================== КАПУСТА КРАСНОКОЧАННАЯ (1) ====================
        cabbage_red = [
            SeedVariety(name="РЕДГАРД F1", category="капуста краснокочанная", variety_type="гибрид F1"),
        ]
        self.seeds.extend(cabbage_red)

        # ==================== КУКУРУЗА САХАРНАЯ (11) ====================
        corn = [
            SeedVariety(name="РАКЕЛЬ F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="КАМБЕРЛЕНД F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="МИНТ F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="КАМУК F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="КОПА F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="ТУРБИН F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="ОВАТОНА F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="НИКОЛЬ F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="МЕГАТОН F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="ДРАЙВЕР F1", category="кукуруза сахарная", variety_type="гибрид F1"),
            SeedVariety(name="КЕТАМА F1", category="кукуруза сахарная", variety_type="гибрид F1"),
        ]
        self.seeds.extend(corn)

        # ==================== АРБУЗ (3) ====================
        watermelons = [
            SeedVariety(name="ЛИВИЯ F1", category="арбуз", variety_type="гибрид F1"),
            SeedVariety(name="ЭПИКА F1", category="арбуз", variety_type="гибрид F1"),
            SeedVariety(name="ЦЕЛИН F1", category="арбуз", variety_type="гибрид F1"),
        ]
        self.seeds.extend(watermelons)

        # ==================== БАКЛАЖАН (3) ====================
        eggplants = [
            SeedVariety(name="ФАБИНА F1", category="баклажан", variety_type="гибрид F1"),
            SeedVariety(name="КАЗИМИР F1", category="баклажан", variety_type="гибрид F1"),
            SeedVariety(name="КЛАССИК F1", category="баклажан", variety_type="гибрид F1"),
        ]
        self.seeds.extend(eggplants)

        # ==================== БРОККОЛИ (3) ====================
        broccolis = [
            SeedVariety(name="ВАВИЛОН F1", category="брокколи", variety_type="гибрид F1"),
            SeedVariety(name="КОРОС F1", category="брокколи", variety_type="гибрид F1"),
            SeedVariety(name="СИГНО F1", category="брокколи", variety_type="гибрид F1"),
        ]
        self.seeds.extend(broccolis)

        # ==================== ДЫНЯ (3) ====================
        melons = [
            SeedVariety(name="МАОРИ F1", category="дыня", variety_type="гибрид F1"),
            SeedVariety(name="МАЗИН F1", category="дыня", variety_type="гибрид F1"),
            SeedVariety(name="МАБЕЛЛА F1", category="дыня", variety_type="гибрид F1"),
        ]
        self.seeds.extend(melons)

        # ==================== КАБАЧОК (3) ====================
        zucchinis = [
            SeedVariety(name="ЯСНА F1", category="кабачок", variety_type="гибрид F1"),
            SeedVariety(name="СУПЕР ДОНИЯ F1", category="кабачок", variety_type="гибрид F1"),
            SeedVariety(name="АСМА F1", category="кабачок", variety_type="гибрид F1"),
        ]
        self.seeds.extend(zucchinis)

        # ==================== ТЫКВА (7) ====================
        pumpkins = [
            SeedVariety(name="ГЛАДИАТОР F1", category="тыква", variety_type="гибрид F1"),
            SeedVariety(name="СПИТФАЕР F1", category="тыква", variety_type="гибрид F1"),
            SeedVariety(name="СИБЕЛЬ F1", category="тыква", variety_type="гибрид F1"),
            SeedVariety(name="РУЖ ВИФ ДЕ ТАМП", category="тыква", variety_type="сорт"),
            SeedVariety(name="ГОМЕС F1", category="тыква", variety_type="гибрид F1"),
            SeedVariety(name="КРАНЧИК F1", category="тыква", variety_type="гибрид F1"),
            SeedVariety(name="МУСКАТ ДЕ ПРОВАНС", category="тыква", variety_type="сорт"),
        ]
        self.seeds.extend(pumpkins)

        # ==================== ПЕТРУШКА (1) ====================
        parsley = [
            SeedVariety(name="НОВАС", category="петрушка", variety_type="сорт"),
        ]
        self.seeds.extend(parsley)

        # ==================== РЕДИС (1) ====================
        radishes = [
            SeedVariety(name="ДЖОЛЛИ", category="редис", variety_type="сорт"),
        ]
        self.seeds.extend(radishes)

        # ==================== СВЕКЛА СТОЛОВАЯ (1) ====================
        beets = [
            SeedVariety(name="НОБОЛ", category="свекла столовая", variety_type="сорт"),
        ]
        self.seeds.extend(beets)

        # ==================== СПАРЖЕВАЯ ФАСОЛЬ (3) ====================
        beans = [
            SeedVariety(name="АЛДРИН", category="спаржевая фасоль", variety_type="сорт"),
            SeedVariety(name="КРОКЕТ", category="спаржевая фасоль", variety_type="сорт"),
            SeedVariety(name="КАПРИЗ", category="спаржевая фасоль", variety_type="сорт"),
        ]
        self.seeds.extend(beans)

        # ==================== ЦВЕТНАЯ КАПУСТА (4) ====================
        cauliflower = [
            SeedVariety(name="САБОРД F1", category="цветная капуста", variety_type="гибрид F1"),
            SeedVariety(name="ДЮРОК F1", category="цветная капуста", variety_type="гибрид F1"),
            SeedVariety(name="АРДЕНТ F1", category="цветная капуста", variety_type="гибрид F1"),
            SeedVariety(name="НАУТИЛУС F1", category="цветная капуста", variety_type="гибрид F1"),
        ]
        self.seeds.extend(cauliflower)

        # ==================== ОГУРЕЦ (3) ====================
        cucumbers = [
            SeedVariety(name="АНВАР F1", category="огурец", variety_type="гибрид F1"),
            SeedVariety(name="РЕГАЛ F1", category="огурец", variety_type="гибрид F1"),
            SeedVariety(name="ЯГУАР F1", category="огурец", variety_type="гибрид F1"),
        ]
        self.seeds.extend(cucumbers)

    # ==================== МЕТОДЫ ПОИСКА ====================

    def get_seeds_by_category(self, category: str) -> List[SeedVariety]:
        """Получить семена по категории"""
        return [s for s in self.seeds if s.category.lower() == category.lower()]

    def get_seed_by_name(self, name: str) -> Optional[SeedVariety]:
        """Найти семя по названию"""
        name_lower = name.lower().strip()
        for seed in self.seeds:
            if seed.name.lower() == name_lower:
                return seed
        # Частичное совпадение
        for seed in self.seeds:
            if name_lower in seed.name.lower() or seed.name.lower() in name_lower:
                return seed
        return None

    def get_all_categories(self) -> List[str]:
        """Получить все категории"""
        categories = {}
        for seed in self.seeds:
            cat = seed.category
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        return categories

    def get_total_count(self) -> int:
        """Общее количество семян"""
        return len(self.seeds)

    def search_seeds(self, query: str) -> List[SeedVariety]:
        """Поиск семян по запросу"""
        query_lower = query.lower()
        results = []
        for seed in self.seeds:
            if (query_lower in seed.name.lower() or
                    query_lower in seed.category.lower() or
                    query_lower in seed.description.lower()):
                results.append(seed)
        return results


# Глобальный экземпляр
seeds_db = SeedsDatabase()
