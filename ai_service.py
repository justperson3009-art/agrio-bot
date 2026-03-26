import logging
import re
import aiohttp
import hashlib
import time
from datetime import datetime
from typing import List, Dict
from config import QWEN_API_KEY, QWEN_MODEL, QWEN_LOCAL, OLLAMA_URL
from prompts import SYSTEM_PROMPT, MAX_RESPONSE_LENGTH, API_TIMEOUT
from seeds_database import seeds_db, SeedVariety

logger = logging.getLogger(__name__)


class AIAgroConsultant:
    """Класс для работы с Qwen API (локально или облако)"""

    def __init__(self):
        self.api_key = QWEN_API_KEY
        self.model = QWEN_MODEL or "qwen2.5:7b"
        self.local_mode = QWEN_LOCAL  # Уже булево из config.py

        if self.local_mode:
            # Локальный Ollama - используем /api/chat для messages
            self.url = OLLAMA_URL.replace("/api/generate", "/api/chat") or "http://localhost:11434/api/chat"
            logger.info(f"Qwen локальный режим: {self.model} на {self.url}")
        else:
            # Облако Alibaba DashScope
            self.url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
            logger.info(f"Qwen облачный режим: {self.model}")
        
        # Кэш ответов ИИ
        self.response_cache = {}
        self.cache_ttl = 3600  # 1 час

        # Connection pool
        self._session = None

    def is_purchase_request(self, user_message: str) -> bool:
        """Проверка: пользователь спрашивает где купить/найти семена?"""
        purchase_keywords = [
            'купить', 'где найти', 'где приобрести', 'приобрести', 'взять',
            'заказать', 'заказ', 'магазин', 'адрес', 'сайт', 'ссылк',
            'ozon', 'озон', 'доставк', 'оплат', 'цена', 'стоимост', 'сколько стоит'
        ]
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in purchase_keywords)

    def get_purchase_info(self, user_message: str) -> str:
        """Вернуть информацию о покупке без ИИ"""
        info = "🏪 **Где купить семена AGRIO:**\n\n"
        info += "🌐 **Сайт:** agrio.by\n"
        info += "📦 **Ozon:** ozon.by/seller/agrio/\n"
        info += "📦 **Wildberries:** wildberries.ru/catalog/327815053\n\n"
        info += "💡 **Доставка:** по всей Беларуси и России\n"

        current_month = datetime.now().month
        month_seeds = self.get_seeds_for_month(current_month)

        if month_seeds:
            info += "\n\n🌱 **Что сажать в этом месяце:**\n\n"
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

    def _get_cache_key(self, message: str) -> str:
        """Получить ключ кэша"""
        return hashlib.md5(message.lower().encode()).hexdigest()

    def _get_cached_response(self, message: str) -> str:
        """Получить ответ из кэша"""
        cache_key = self._get_cache_key(message)
        if cache_key in self.response_cache:
            cached = self.response_cache[cache_key]
            if time.time() - cached['time'] < self.cache_ttl:
                logger.debug(f"Кэш hit для: {message[:50]}")
                return cached['response']
            else:
                del self.response_cache[cache_key]
        return None

    def _save_to_cache(self, message: str, response: str):
        """Сохранить ответ в кэш"""
        cache_key = self._get_cache_key(message)
        self.response_cache[cache_key] = {
            'response': response,
            'time': time.time()
        }
        logger.debug(f"Кэш saved для: {message[:50]}")

    async def _get_session(self) -> aiohttp.ClientSession:
        """Получить сессию"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=10, ttl_dns_cache=300)
            )
        return self._session

    async def close(self):
        """Закрыть сессию"""
        if self._session and not self._session.closed:
            await self._session.close()

    def get_seed_recommendations(self, user_message: str) -> str:
        """Получить рекомендации по семенам из базы"""
        message_lower = user_message.lower()
        category = None
        criteria = {}

        categories_map = {
            'томат': 'томат', 'помидор': 'томат', 'томаты': 'томат',
            'перец': 'перец', 'перцы': 'перец',
            'морковь': 'морковь', 'морковка': 'морковь',
            'капуста': 'капуста белокочанная',
            'арбуз': 'арбуз', 'арбузы': 'арбуз',
            'кабачок': 'кабачок', 'кабачки': 'кабачок',
            'тыква': 'тыква',
            'брокколи': 'брокколи',
            'дыня': 'дыня',
            'баклажан': 'баклажан', 'баклажаны': 'баклажан',
            'огурец': 'огурец', 'огурцы': 'огурец',
            'кукуруза': 'кукуруза сахарная',
            'фасоль': 'спаржевая фасоль',
            'свекла': 'свекла столовая',
            'редис': 'редис',
            'петрушка': 'петрушка',
        }

        for key, value in categories_map.items():
            if key in message_lower:
                category = value
                break

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

        if not category:
            keywords = message_lower.split()
            search_results = seeds_db.search_by_features(keywords)
            if search_results:
                result = "🌱 **Рекомендуемые сорта AGRIO:**\n\n"
                for i, seed in enumerate(search_results[:5], 1):
                    result += f"{i}. **{seed.name}** ({seed.category})\n"
                    if seed.ripening_period:
                        result += f"   📅 {seed.ripening_period}\n"
                    if seed.fruit_weight:
                        result += f"   ⚖️ {seed.fruit_weight}\n"
                    if seed.description:
                        result += f"   {seed.description}\n"
                    result += "\n"
                return result

        if category:
            recommendations = seeds_db.get_recommendations_for_category(category, criteria)
            if recommendations:
                category_name = category.replace(' ', '_').replace('белокочанная', '').strip('_')
                result = f"🌱 **Рекомендуемые сорта: {category.upper()}**\n\n"

                for i, seed in enumerate(recommendations, 1):
                    result += f"{i}. **{seed.name}** ({seed.variety_type})\n"
                    if seed.ripening_period:
                        result += f"   📅 {seed.ripening_period}\n"
                    if seed.fruit_weight:
                        result += f"   ⚖️ {seed.fruit_weight}\n"
                    if seed.features:
                        for feature in seed.features[:3]:
                            result += f"   • {feature}\n"
                    if seed.growing_conditions:
                        result += f"   🏡 {seed.growing_conditions}\n"
                    result += "\n"
                return result
        return ""

    async def get_consultation(
        self,
        user_message: str,
        dialog_context: List[Dict[str, str]] = None
    ) -> str:
        """Получить консультацию от ИИ-агронома"""
        if self.is_purchase_request(user_message):
            logger.info("Запрос о покупке — возвращаем информацию без ИИ")
            return self.get_purchase_info(user_message)

        cached = self._get_cached_response(user_message)
        if cached:
            return cached

        seed_recommendations = self.get_seed_recommendations(user_message)
        system_prompt = SYSTEM_PROMPT
        
        if seed_recommendations:
            system_prompt += f"\n\n🌱 ДОП. ДАННЫЕ О СЕМЕНАХ:\n{seed_recommendations}"

        if self.local_mode:
            # ЛОКАЛЬНЫЙ РЕЖИМ (Ollama)
            return await self._get_consultation_local(user_message, system_prompt, dialog_context)
        else:
            # ОБЛАЧНЫЙ РЕЖИМ (DashScope)
            return await self._get_consultation_cloud(user_message, system_prompt, dialog_context)

    async def _get_consultation_local(
        self,
        user_message: str,
        system_prompt: str,
        dialog_context: List[Dict[str, str]] = None
    ) -> str:
        """Запрос к локальной Qwen модели через Ollama"""
        # Формируем промпт
        messages = [{"role": "system", "content": system_prompt}]
        
        if dialog_context:
            for msg in dialog_context:
                role = "assistant" if msg["role"] == "assistant" else msg["role"]
                messages.append({"role": role, "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_message})

        # Тело запроса для Ollama
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 1500
            }
        }

        headers = {"Content-Type": "application/json"}

        try:
            session = await self._get_session()
            async with session.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
            ) as response:
                result = await response.json()

                if response.status != 200:
                    logger.error(f"Ошибка Ollama API: {result}")
                    return "Извините, произошла ошибка. Попробуйте позже."

                # Ollama возвращает ответ в формате {"response": "..."} для /api/generate
                # или {"message": {"content": "..."}} для /api/chat
                answer = result.get("response", "") or result.get("message", {}).get("content", "")
                
                # Логирование для отладки
                logger.info(f"Ollama result keys: {list(result.keys())}")
                logger.info(f"Ollama full result: {result}")

                logger.info(f"Qwen локальный ответ: {answer[:500]}...")
                logger.info(f"Длина ответа: {len(answer)} символов")

                if not answer:
                    return "Извините, не удалось получить ответ."

                if len(answer) > MAX_RESPONSE_LENGTH:
                    answer = answer[:MAX_RESPONSE_LENGTH - 3] + "..."

                self._save_to_cache(user_message, answer)
                logger.info(f"ИИ ответ: {answer[:100]}...")
                return answer

        except Exception as e:
            logger.error(f"Ошибка при запросе к локальной Qwen: {e}")
            return "Извините, произошла ошибка. Попробуйте позже."

    async def _get_consultation_cloud(
        self,
        user_message: str,
        system_prompt: str,
        dialog_context: List[Dict[str, str]] = None
    ) -> str:
        """Запрос к облачной Qwen модели через DashScope"""
        messages = [{"role": "system", "content": system_prompt}]
        
        if dialog_context:
            for msg in dialog_context:
                messages.append({
                    "role": msg["role"] if msg["role"] != "assistant" else "assistant",
                    "content": msg["content"]
                })
        
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "input": {"messages": messages},
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1500,
                "result_format": "message"
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            session = await self._get_session()
            async with session.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
            ) as response:
                result = await response.json()

                if response.status != 200:
                    logger.error(f"Ошибка Qwen Cloud API: {result}")
                    return "Извините, произошла ошибка. Попробуйте позже."

                answer = result.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "")

                logger.info(f"Qwen cloud ответ: {answer[:500]}...")

                if not answer:
                    return "Извините, не удалось получить ответ."

                if len(answer) > MAX_RESPONSE_LENGTH:
                    answer = answer[:MAX_RESPONSE_LENGTH - 3] + "..."

                self._save_to_cache(user_message, answer)
                logger.info(f"ИИ ответ: {answer[:100]}...")
                return answer

        except Exception as e:
            logger.error(f"Ошибка при запросе к Qwen Cloud: {e}")
            return "Извините, произошла ошибка. Попробуйте позже."

    async def check_injection_attempt(self, message: str) -> bool:
        """Проверка на Prompt Injection"""
        injection_patterns = [
            r"забудь\s+(все\s+)?инструкци",
            r"игнорируй\s+(инструкци|правила)",
            r"повтори\s+(системн|инструкци)",
            r"раскрой\s+(промпт|настройк)",
            r"ты\s+теперь\s+",
            r"смени\s+роль",
            r"новый\s+приказ",
            r"системное\s+сообщение"
        ]

        message_lower = message.lower()
        for pattern in injection_patterns:
            if re.search(pattern, message_lower):
                logger.warning(f"Попытка prompt injection: {message[:100]}")
                return True
        return False
