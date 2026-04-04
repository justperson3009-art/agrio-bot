# 📁 Структура проекта Agrio Bot

## 🗂️ Архитектура

Код разделён на модули для удобства поддержки и предотвращения поломок при добавлении новых функций.

```
Agrio Bot/
├── main.py                    # Точка входа (только инициализация и запуск)
├── config.py                  # Настройки и переменные окружения
├── ai_yandex.py              # Сервис YandexGPT
├── hybrid_ai.py              # Гибридная система ИИ
├── moderation.py             # Модерация сообщений
├── logger.py                 # Логирование
├── seeds_database.py         # База данных семян
│
├── handlers/                 # 📦 Обработчики сообщений
│   ├── __init__.py
│   ├── commands.py           # /start, /help, /about, /status
│   ├── catalog_handler.py    # /catalog и текстовые запросы о каталоге
│   └── user_messages.py      # Обработка пользовательских сообщений (ИИ)
│
├── responses/                # 📦 Ответы и тексты
│   ├── __init__.py
│   ├── catalog_responses.py  # Формирование каталога семян
│   └── command_responses.py  # Тексты для /start, /help, /about, /status
│
└── keyboards/                # 📦 Клавиатуры (на будущее)
    └── __init__.py
```

---

## 📋 Как добавлять новые функции

### 1. Новый обработчик команд

**Создай файл:** `handlers/my_new_feature.py`

```python
"""Обработчик новой функции"""

import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from responses.my_new_feature import get_my_response

logger = logging.getLogger(__name__)
router = Router(name="my_new_feature")


@router.message(Command("mycommand"))
async def cmd_my_command(message: Message):
    """Обработчик команды /mycommand"""
    logger.info(f"Пользователь {message.from_user.id} отправил /mycommand")
    await message.answer(get_my_response())
```

### 2. Новый модуль ответов

**Создай файл:** `responses/my_new_feature.py`

```python
"""Ответы для новой функции"""


def get_my_response() -> str:
    """Текст ответа"""
    return "🌱 Это ответ новой функции!"
```

### 3. Зарегистрируй роутер

**Добавь в `main.py`:**

```python
# Импорт роутеров
from handlers.my_new_feature import router as my_new_router

# В main():
dp.include_router(my_new_router)
```

### 4. Обнови `__init__.py`

**В `handlers/__init__.py`:**

```python
from .my_new_feature import router as my_new_router
```

---

## 🎯 Преимущества такой структуры

| Было | Стало |
|------|-------|
| Один файл 500+ строк | Модули по 50-150 строк |
| Сложно найти код | Чёткое разделение |
| Легко сломать | Изолированные изменения |
| Тестирование затруднено | Каждый модуль тестируется отдельно |

---

## 🔧 Где что менять

### Изменить текст /start или /help?
→ `responses/command_responses.py`

### Добавить новый сорт в каталог?
→ `responses/catalog_responses.py`

### Добавить новую команду?
→ `handlers/новый_файл.py` + `main.py` (регистрация роутера)

### Изменить логику обработки сообщений?
→ `handlers/user_messages.py`

### Изменить ответы ИИ?
→ `hybrid_ai.py` или `ai_yandex.py`

---

## 🧪 Тестирование модулей

Каждый модуль можно тестировать отдельно:

```python
# Тест модуля ответов
from responses.catalog_responses import get_catalog_response

print(get_catalog_response())  # Проверяем формирование каталога
```

```python
# Тест обработчика команд
from responses.command_responses import get_start_response

print(get_start_response())  # Проверяем текст /start
```

---

## 📈 Масштабирование

### Когда добавится много функций:

```
handlers/
├── commands/           # Папка с командами
│   ├── start.py
│   ├── help.py
│   ├── about.py
│   └── status.py
├── catalog/            # Каталог и семена
│   ├── catalog_cmd.py
│   └── seed_info.py
└── user_messages.py    # Общие сообщения

responses/
├── commands/           # Ответы на команды
│   ├── start_resp.py
│   ├── help_resp.py
│   └── about_resp.py
├── catalog/            # Ответы о каталоге
│   ├── catalog_resp.py
│   └── seed_resp.py
└── common.py           # Общие ответы
```

---

## ✅ Чек-лист при добавлении функции

- [ ] Создан файл обработчика в `handlers/`
- [ ] Создан файл ответов в `responses/` (если нужно)
- [ ] Добавлен роутер в `handlers/__init__.py`
- [ ] Зарегистрирован роутер в `main.py`
- [ ] Проверен синтаксис: `python -m py_compile handlers/новый_файл.py`
- [ ] Обновлена документация
- [ ] Протестирована функция

---

**Версия:** 2.2 (апрель 2026)
**Архитектура:** Модульная
