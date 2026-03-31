# 🧹 Очистка сервера от Qwen

**Дата:** 31 марта 2026  
**Версия:** 2.1

---

## 📋 ШАГИ ПО ОЧИСТКЕ

### ШАГ 1: Подключение к серверу

```powershell
ssh root@93.84.121.179
```
**Пароль:** `79599687959968!`

---

### ШАГ 2: Проверка текущего состояния

```bash
# Проверка места на диске
df -h /

# Проверка оперативной памяти
free -h

# Перейти в директорию бота
cd /opt/agrio-bot

# Посмотреть размер проекта
du -sh /opt/agrio-bot
```

---

### ШАГ 3: Остановка Ollama (если запущен)

```bash
# Проверка статуса Ollama
systemctl status ollama

# Если запущен - остановить и отключить
systemctl stop ollama
systemctl disable ollama
```

---

### ШАГ 4: Удаление Ollama и моделей Qwen

```bash
# Проверить установлен ли Ollama
which ollama

# Удалить Ollama
rm -f /usr/local/bin/ollama
rm -rf /usr/share/ollama
rm -rf ~/.ollama

# Удалить сервис systemd
rm -f /etc/systemd/system/ollama.service
systemctl daemon-reload

# Проверить модели (если остались)
ollama list 2>/dev/null || echo "Ollama удалён"
```

---

### ШАГ 5: Обновление кода бота

```bash
cd /opt/agrio-bot

# Бэкап .env
cp .env .env.backup

# Обновление из GitHub
git pull origin main

# Проверка изменений
git log --oneline -3
```

---

### ШАГ 6: Проверка .env (удалить Qwen настройки)

```bash
# Просмотреть .env
cat .env
```

**Удалить строки (если есть):**
```
QWEN_API_KEY=...
QWEN_MODEL=...
QWEN_LOCAL=...
OLLAMA_URL=...
QWEN_MODEL_LOCAL=...
```

**Оставить только:**
```env
# Telegram Bot Token
BOT_TOKEN=...

# YandexGPT API
YANDEX_KEY_ID=...
YANDEX_SECRET_KEY=...
YANDEX_FOLDER_ID=...

# Администратор
ADMIN_ID=...
ALLOWED_CHAT_IDS=...

# Настройки чатов
CHAT_MENTION_ONLY=...
CHAT_AGRO_MODE=...
```

---

### ШАГ 7: Удаление лишних файлов на сервере

```bash
cd /opt/agrio-bot

# Удалить тестовый файл Ollama
rm -f test_ollama.py

# Удалить документацию по Qwen (не обязательные файлы)
rm -f INSTALL_LOCAL_QWEN.md
rm -f LOCAL_QWEN.md
rm -f QWEN_SETUP.md

# Проверка размера после очистки
du -sh /opt/agrio-bot
```

---

### ШАГ 8: Перезапуск бота

```bash
cd /opt/agrio-bot

# Перезапуск сервиса
systemctl restart agrio-bot

# Проверка статуса
systemctl status agrio-bot

# Просмотр логов
journalctl -u agrio-bot -f
```

---

### ШАГ 9: Проверка работы

**В Telegram:**
1. Написать боту: `/start`
2. Написать: `Каталог`
3. Написать: `Когда сажать томаты?`

**Ожидание:** Бот отвечает мгновенно (из базы знаний) или через 2-3 сек (YandexGPT)

---

## 📊 Освобождённое место

| Что удаляем | Размер |
|-------------|--------|
| Ollama бинарник | ~100 MB |
| Модель Qwen 7B | ~4.7 GB |
| Модель Qwen 14B | ~9 GB |
| Кэш Ollama | ~500 MB |
| Файлы проекта | ~50 MB |
| **Итого:** | **~5-14 GB** |

---

## ✅ Чек-лист

- [ ] Подключился к серверу по SSH
- [ ] Проверил место на диске
- [ ] Остановил Ollama
- [ ] Удалил Ollama и модели
- [ ] Обновил код из GitHub
- [ ] Проверил .env (удалил Qwen настройки)
- [ ] Удалил лишние файлы (test_ollama.py, QWEN_*.md)
- [ ] Перезапустил бота
- [ ] Протестировал в Telegram
- [ ] Бот отвечает на "Каталог"

---

## 🆘 Если что-то пошло не так

### Бот не запускается:
```bash
# Проверка логов
journalctl -u agrio-bot -n 50 --no-pager

# Проверка .env
cat /opt/agrio-bot/.env

# Проверка Python
cd /opt/agrio-bot
source venv/bin/activate
python main.py  # Запуск вручную для проверки
```

### Ошибка импорта:
```bash
# Переустановка зависимостей
cd /opt/agrio-bot
source venv/bin/activate
pip install -r requirements.txt
systemctl restart agrio-bot
```

### Ошибка "ai_consultant не определён":
```bash
# Нужно обновить код из GitHub
cd /opt/agrio-bot
git pull origin main
systemctl restart agrio-bot
```

---

## 📁 Файлы которые можно удалить на сервере

**Не обязательные (документация):**
- `INSTALL_LOCAL_QWEN.md`
- `LOCAL_QWEN.md`
- `QWEN_SETUP.md`
- `OPTIMIZATION.md`
- `TODO_PLAN.md`

**Тестовые файлы:**
- `test_ollama.py`

**Обязательные (НЕ удалять):**
- `main.py`
- `config.py`
- `ai_yandex.py`
- `hybrid_ai.py`
- `seeds_database.py`
- `prompts.py`
- `moderation.py`
- `logger.py`
- `.env`
- `requirements.txt`

---

**Готово!** 🎉 Сервер очищен от Qwen, бот работает на гибридной системе!
