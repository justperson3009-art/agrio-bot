import logging
import aiohttp
import hashlib
import time
import jwt
from datetime import datetime, timedelta
from typing import List, Dict
from config import YANDEX_KEY_ID, YANDEX_SECRET_KEY, YANDEX_FOLDER_ID
from prompts import SYSTEM_PROMPT, MAX_RESPONSE_LENGTH, API_TIMEOUT

logger = logging.getLogger(__name__)


class YandexGPTService:
    """Сервис для работы с YandexGPT API (статические ключи + IAM токен)"""

    def __init__(self):
        self.key_id = YANDEX_KEY_ID
        self.secret_key = YANDEX_SECRET_KEY
        self.folder_id = YANDEX_FOLDER_ID
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.iam_token = None
        self.token_expires = None
        
        # Кэш ответов
        self.response_cache = {}
        self.cache_ttl = 3600  # 1 час
        
        # Connection pool
        self._session = None

    def _create_jwt(self) -> str:
        """Создать JWT токен для получения IAM"""
        now = datetime.utcnow()
        payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': self.key_id,
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(minutes=5)).timestamp())
        }
        return jwt.encode(payload, self.secret_key, algorithm='PS256', headers={'kid': self.key_id})

    async def _get_iam_token(self) -> str:
        """Получить IAM токен"""
        # Проверка кэша токена
        if self.iam_token and self.token_expires:
            if datetime.utcnow() < self.token_expires - timedelta(minutes=2):
                return self.iam_token
        
        # Создание JWT
        jwt_token = self._create_jwt()
        
        # Запрос IAM токена
        headers = {'Content-Type': 'application/json'}
        payload = {'jwt': jwt_token}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                result = await response.json()
                
                if response.status != 200:
                    logger.error(f"Ошибка получения IAM токена: {result}")
                    raise Exception(f"Не удалось получить IAM токен: {result}")
                
                self.iam_token = result.get('iamToken', '')
                self.token_expires = datetime.utcnow() + timedelta(minutes=15)
                logger.info("IAM токен получен")
                return self.iam_token

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

    async def get_consultation(
        self,
        user_message: str,
        dialog_context: List[Dict[str, str]] = None
    ) -> str:
        """Получить консультацию от YandexGPT"""
        
        # Проверка кэша
        cached = self._get_cached_response(user_message)
        if cached:
            return cached

        # Формирование сообщений для API
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if dialog_context:
            for msg in dialog_context:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        messages.append({"role": "user", "content": user_message})

        # Тело запроса к YandexGPT
        payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 1500
            },
            "messages": messages
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {await self._get_iam_token()}"
        }

        try:
            logger.info(f"YandexGPT запрос: folder_id={self.folder_id}")
            logger.info(f"Сообщений в запросе: {len(messages)}")

            session = await self._get_session()
            async with session.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
            ) as response:
                result = await response.json()

                if response.status != 200:
                    logger.error(f"Ошибка YandexGPT API: {result}")
                    return "Извините, произошла ошибка. Попробуйте позже."

                # Парсинг ответа
                answer = result.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "")

                logger.info(f"YandexGPT ответ: {answer[:500]}...")

                if not answer:
                    return "Извините, не удалось получить ответ."

                # Ограничение длины ответа
                if len(answer) > MAX_RESPONSE_LENGTH:
                    answer = answer[:MAX_RESPONSE_LENGTH - 3] + "..."

                self._save_to_cache(user_message, answer)
                logger.info(f"ИИ ответ: {answer[:100]}...")
                return answer

        except aiohttp.ClientTimeout:
            logger.error("Таймаут запроса к YandexGPT")
            return "Извините, запрос слишком долгий. Попробуйте позже."
        except Exception as e:
            logger.error(f"Ошибка при запросе к YandexGPT: {e}")
            return "Извините, произошла ошибка. Попробуйте позже."
