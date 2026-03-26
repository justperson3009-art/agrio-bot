# 🚀 УСТАНОВКА LОКАЛЬНОЙ QWEN НА СЕРВЕРЕ

## 📋 Инструкция (выполнять на сервере Proxmox)

---

## ШАГ 1: Проверка ресурсов сервера

```bash
# Оперативная память
free -h

# Место на диске
df -h /

# Количество ядер CPU
nproc
```

**Минимальные требования:**
- RAM: 8GB (для модели 7B)
- CPU: 4 ядра
- Место: 10GB

---

## ШАГ 2: Установка Ollama

```bash
# Установка Ollama (одна команда)
curl -fsSL https://ollama.com/install.sh | sh

# Проверка установки
ollama --version
```

---

## ШАГ 3: Запуск Ollama сервиса

```bash
# Создание systemd сервиса
cat > /etc/systemd/system/ollama.service << 'EOF'
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=10
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

# Применение изменений
systemctl daemon-reload
systemctl enable ollama
systemctl start ollama

# Проверка статуса
systemctl status ollama
```

---

## ШАГ 4: Загрузка Qwen модели

```bash
# Для серверов с 8GB RAM (модель 7B)
ollama pull qwen2.5:7b

# ИЛИ для серверов с 16GB RAM (модель 14B)
# ollama pull qwen2.5:14b

# ИЛИ для серверов с 4GB RAM (модель 3B)
# ollama pull qwen2.5:3b
```

**Проверка загрузки:**
```bash
ollama list
```

Должно показать:
```
NAME              ID           SIZE
qwen2.5:7b        ...          4.7 GB
```

---

## ШАГ 5: Тестирование Qwen

```bash
# Быстрый тест
ollama run qwen2.5:7b "Привет! Как дела?"
```

Должен появиться ответ от ИИ.

---

## ШАГ 6: Обновление бота Agrio

```bash
cd /opt/agrio-bot

# Обновление кода из GitHub
git pull origin main

# Деактивация venv (если активирован)
deactivate 2>/dev/null || true

# Активация venv
source venv/bin/activate

# Проверка что зависимости установлены (не нужны новые)
pip list | grep -E "aiogram|aiohttp"
```

---

## ШАГ 7: Настройка .env для локальной работы

```bash
cd /opt/agrio-bot

# Редактирование .env
nano .env
```

**Добавьте в конец файла:**
```
# Локальная Qwen модель
QWEN_LOCAL=true
QWEN_MODEL=qwen2.5:7b
OLLAMA_URL=http://localhost:11434/api/generate
```

**Сохраните:** `Ctrl+O` → `Enter` → `Ctrl+X`

---

## ШАГ 8: Перезапуск бота

```bash
# Перезапуск сервиса бота
systemctl restart agrio-bot

# Проверка статуса
systemctl status agrio-bot

# Просмотр логов
journalctl -u agrio-bot -f
```

**Должно быть:**
```
Qwen локальный режим: qwen2.5:7b на http://localhost:11434/api/generate
Бот авторизован: @Agrio_Bot
Бот запускается...
```

---

## ШАГ 9: Тестирование бота

1. Откройте Telegram
2. Найдите вашего бота
3. Отправьте: `Когда сажать томаты на рассаду?`
4. Бот должен ответить с рекомендациями

---

## 🔧 Управление Ollama

```bash
# Статус
systemctl status ollama

# Перезапуск
systemctl restart ollama

# Логи
journalctl -u ollama -f

# Остановка
systemctl stop ollama

# Запуск
systemctl start ollama
```

---

## 📊 Мониторинг ресурсов

```bash
# Использование RAM моделью
ollama ps

# Список моделей
ollama list

# Тест скорости
ollama run qwen2.5:7b "Расскажи кратко о посадке томатов"
```

---

## ⚠️ Возможные проблемы

### Ошибка "Could not find model"

```bash
# Проверьте название модели
ollama list

# Если пусто, загрузите:
ollama pull qwen2.5:7b
```

### Ошибка "Connection refused"

```bash
# Проверьте что Ollama запущен
systemctl status ollama

# Если не запущен:
systemctl start ollama
```

### Бот не отвечает

```bash
# Проверьте логи бота
journalctl -u agrio-bot -f

# Проверьте что Ollama работает
ollama ps

# Перезапустите бота
systemctl restart agrio-bot
```

### Недостаточно RAM

```bash
# Используйте меньшую модель
ollama pull qwen2.5:3b

# Обновите .env
nano .env
# QWEN_MODEL=qwen2.5:3b

systemctl restart agrio-bot
```

---

## 📝 Быстрая установка (все команды сразу)

```bash
# 1. Установка Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Настройка сервиса
cat > /etc/systemd/system/ollama.service << 'EOF'
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=10
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ollama
systemctl start ollama

# 3. Загрузка модели
ollama pull qwen2.5:7b

# 4. Обновление бота
cd /opt/agrio-bot
git pull origin main

# 5. Настройка .env
echo -e "\n# Local Qwen\nQWEN_LOCAL=true\nQWEN_MODEL=qwen2.5:7b\nOLLAMA_URL=http://localhost:11434/api/generate" >> .env

# 6. Перезапуск бота
systemctl restart agrio-bot

# 7. Проверка
systemctl status agrio-bot
journalctl -u agrio-bot -f
```

---

## ✅ Чеклист успешной установки

- [ ] Ollama установлен (`ollama --version`)
- [ ] Сервис запущен (`systemctl status ollama`)
- [ ] Модель загружена (`ollama list`)
- [ ] Тест работает (`ollama run qwen2.5:7b "Привет"`)
- [ ] Бот обновлён (`git pull`)
- [ ] .env настроен (`QWEN_LOCAL=true`)
- [ ] Бот перезапущен (`systemctl restart agrio-bot`)
- [ ] Бот отвечает в Telegram

---

## 💡 Преимущества локальной установки

| Параметр | Облако | Локально |
|----------|--------|----------|
| Стоимость | Бесплатно (лимиты) | Бесплатно |
| Лимиты | 500K токенов/мес | Безлимитно |
| Скорость | Зависит от интернета | Максимальная |
| Приватность | Данные у провайдера | Данные у вас |
| Доступ | Нужен интернет | Работает офлайн |

---

**Готово!** Qwen работает локально на вашем сервере! 🎉
