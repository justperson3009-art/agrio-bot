from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import aiohttp
import logging
from datetime import datetime
from config import ADMIN_ID, WEATHER_API_KEY

router = Router()
logger = logging.getLogger(__name__)

# OpenWeatherMap API кэш
WEATHER_CACHE = {}
WEATHER_CACHE_TTL = 1800  # 30 минут

async def get_weather(city: str = "Minsk") -> dict:
    """Получить погоду для города"""
    import hashlib
    cache_key = hashlib.md5(city.lower().encode()).hexdigest()
    
    if cache_key in WEATHER_CACHE:
        cached = WEATHER_CACHE[cache_key]
        from time import time
        if time() - cached['time'] < WEATHER_CACHE_TTL:
            return cached['data']
    
    if not WEATHER_API_KEY:
        return None
    
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    from time import time
                    WEATHER_CACHE[cache_key] = {'data': data, 'time': time()}
                    return data
    except Exception as e:
        logger.error(f"Ошибка получения погоды: {e}")
    
    return None

def get_weather_advice(data: dict) -> str:
    """Получить сельскохозяйственный совет по погоде"""
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    desc = data['weather'][0]['description']
    city = data['name']
    
    advice = f"🌤️ **ПОГОДА: {city}**\n\n"
    advice += f"🌡️ Температура: {temp:.0f}°C ({temp_min:.0f}...{temp_max:.0f}°C)\n"
    advice += f"💧 Влажность: {humidity}%\n"
    advice += f"💨 Ветер: {wind:.1f} м/с\n"
    advice += f"☁️ {desc.capitalize()}\n\n"
    
    # Сельскохозяйственные советы
    warnings = []
    tips = []
    
    # Заморозки
    if temp_min <= 0:
        warnings.append("❄️ **ЗАМОРОЗКИ!** Укройте теплолюбивые растения!")
        tips.append("🛡️ Спанбонд на дуги")
        tips.append("💧 Обильный вечерний полив")
        tips.append("🔥 Дымление (для больших площадей)")
    
    # Жара
    if temp_max >= 30:
        warnings.append("🌡️ **ЖАРА!** Притените растения!")
        tips.append("🌿 Мульча обязательно!")
        tips.append("💧 Полив утром И вечером")
        tips.append("🏡 Проветривайте теплицу")
    
    if temp >= 35:
        warnings.append("⚠️ При +35°C пыльца томатов стерильна!")
    
    # Дождь
    if 'rain' in desc or 'дождь' in desc.lower():
        tips.append("🌧️ Полив можно отложить!")
        tips.append("⚠️ Проверьте теплицу на протечки")
    
    # Высокая влажность
    if humidity >= 85:
        warnings.append("💧 Высокая влажность — риск фитофторы!")
        tips.append("🧪 Профилактика: Фитоспорин")
        tips.append("🌬️ Проветривайте теплицу")
    
    # Низкая влажность
    if humidity <= 30:
        tips.append("💨 Сухой воздух — участите полив")
    
    # Ветер
    if wind >= 10:
        warnings.append(f"💨 Сильный ветер ({wind:.1f} м/с)!")
        tips.append("🏡 Закройте форточки теплицы")
        tips.append("🌿 Подвяжите высокие растения")
    
    # Нормальная погода
    if not warnings and not tips:
        tips.append("✅ Отличная погода для огородных работ!")
        if 15 <= temp <= 25:
            tips.append("🌱 Идеально для высадки рассады")
    
    if warnings:
        advice += "⚠️ **ПРЕДУПРЕЖДЕНИЯ:**\n"
        for w in warnings:
            advice += f"{w}\n"
        advice += "\n"
    
    if tips:
        advice += "💡 **РЕКОМЕНДАЦИИ:**\n"
        for t in tips:
            advice += f"{t}\n"
    
    return advice

@router.message(Command('weather'))
async def cmd_weather(message: Message):
    """Погода и сельскохозяйственный совет"""
    parts = message.text.split()
    city = 'Minsk'
    if len(parts) > 1:
        city = ' '.join(parts[1:])
    
    weather_data = await get_weather(city)
    
    if weather_data is None:
        if not WEATHER_API_KEY:
            await message.answer(
                "🌤️ **Погода**\n\n"
                "⚠️ API ключ не настроен.\n"
                "Получите ключ на openweathermap.org/api\n"
                "И добавьте в config.py: WEATHER_API_KEY"
            )
        else:
            await message.answer("❌ Не удалось получить погоду.")
        return
    
    advice = get_weather_advice(weather_data)
    await message.answer(advice)

@router.message(Command('forecast'))
async def cmd_forecast(message: Message):
    """Прогноз на 5 дней"""
    parts = message.text.split()
    city = 'Minsk'
    if len(parts) > 1:
        city = ' '.join(parts[1:])
    
    if not WEATHER_API_KEY:
        await message.answer("⚠️ API ключ погоды не настроен.")
        return
    
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru',
        'cnt': 8  # 8 периодов = 24 часа
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    forecast_text = f"📊 **ПРОГНОЗ: {data['city']['name']}**\n\n"
                    
                    for item in data['list'][:4]:
                        dt = datetime.fromisoformat(item['dt_txt'])
                        temp = item['main']['temp']
                        desc = item['weather'][0]['description']
                        icon = {'clear': '☀️', 'clouds': '☁️', 'rain': '🌧️', 'snow': '❄️'}.get(
                            item['weather'][0]['main'].lower(), '🌤️'
                        )
                        forecast_text += f"{icon} **{dt.strftime('%H:%M')}** — {temp:.0f}°C, {desc}\n"
                    
                    forecast_text += "\n💡 `/weather` — подробный совет"
                    await message.answer(forecast_text)
                else:
                    await message.answer("❌ Ошибка получения прогноза.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@router.message(Command('frost'))
async def cmd_frost(message: Message):
    """Проверка на заморозки"""
    parts = message.text.split()
    city = 'Minsk'
    if len(parts) > 1:
        city = ' '.join(parts[1:])
    
    if not WEATHER_API_KEY:
        await message.answer("⚠️ API ключ погоды не настроен.")
        return
    
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru',
        'cnt': 8
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    frost_found = False
                    frost_msg = ""
                    
                    for item in data['list'][:8]:
                        temp_min = item['main']['temp_min']
                        dt = datetime.fromisoformat(item['dt_txt'])
                        
                        if temp_min <= 2:
                            frost_found = True
                            frost_msg += f"❄️ **{dt.strftime('%d.%m %H:%M')}** — {temp_min:.0f}°C\n"
                    
                    if frost_found:
                        await message.answer(
                            f"❄️ **ПРЕДУПРЕЖДЕНИЕ: ЗАМОРОЗКИ!**\n\n"
                            f"{frost_msg}\n"
                            f"🛡️ **Защита:**\n"
                            f"• Спанбонд на дуги\n"
                            f"• Обильный вечерний полив\n"
                            f"• Дымление (большие площади)"
                        )
                    else:
                        await message.answer("✅ Заморозков в ближайшие 24 часа не ожидается.")
                else:
                    await message.answer("❌ Ошибка.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
