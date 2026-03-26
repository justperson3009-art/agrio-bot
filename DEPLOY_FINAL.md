# 🚀 ДЕПЛОЙ AGRIO БОТА НА СЕРВЕР

## ✅ Код уже на GitHub: https://github.com/justperson3009-art/agrio-bot

---

## 📋 ИНСТРУКЦИЯ (выполнять на сервере)

### ШАГ 1: Подключение к серверу

В PowerShell на компьютере:
```powershell
ssh root@93.84.121.179
```
**Пароль:** `79599687959968!`

---

### ШАГ 2: Клонирование репозитория

```bash
cd /opt
git clone https://github.com/justperson3009-art/agrio-bot.git
cd /opt/agrio-bot
```

---

### ШАГ 3: Создание .env файла

```bash
nano .env
```

**Вставьте содержимое:**
```
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=ваш_id
ALLOWED_CHAT_IDS=разрешённые_chat_id
QWEN_LOCAL=true
QWEN_MODEL=qwen2.5:7b
OLLAMA_URL=http://localhost:11434/api/generate
```

**Сохраните:** `Ctrl+O` → `Enter` → `Ctrl+X`

**Права доступа:**
```bash
chmod 600 .env
```

---

### ШАГ 4: Установка зависимостей

```bash
cd /opt/agrio-bot

# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установка пакетов
pip install --upgrade pip
pip install -r requirements.txt
```

---

### ШАГ 5: Создание systemd сервиса

```bash
cat > /etc/systemd/system/agrio-bot.service << 'EOF'
[Unit]
Description=Agrio Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/agrio-bot
Environment=PATH=/opt/agrio-bot/venv/bin
ExecStart=/opt/agrio-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Применение изменений
systemctl daemon-reload
systemctl enable agrio-bot
systemctl start agrio-bot
```

---

### ШАГ 6: Проверка работы

```bash
# Статус сервиса
systemctl status agrio-bot

# Логи в реальном времени
journalctl -u agrio-bot -f
```

**Проверьте бота в Telegram:**
1. Откройте Telegram
2. Найдите бота по токену
3. Нажмите `/start`
4. Бот должен ответить!

---

## 🔄 ОБНОВЛЕНИЕ КОДА (после изменений)

### На компьютере:
```powershell
cd "C:\Users\user\Desktop\Agrio Bot"

# Проверка изменений
git status

# Коммит
git add -A
git commit -m "Описание изменений"

# Отправка на GitHub
git push
```

### На сервере:
```bash
cd /opt/agrio-bot

# Бэкап .env
cp .env .env.backup

# Получение обновлений
git pull origin main

# Перезапуск бота
systemctl restart agrio-bot

# Проверка логов
journalctl -u agrio-bot -f
```

---

## 📊 КОМАНДЫ УПРАВЛЕНИЯ

```bash
systemctl start agrio-bot      # Запустить
systemctl stop agrio-bot       # Остановить
systemctl restart agrio-bot    # Перезапустить
systemctl status agrio-bot     # Статус

journalctl -u agrio-bot -f     # Логи в реальном времени
journalctl -u agrio-bot -n 50  # Последние 50 строк
```

---

## 🔐 БЕЗОПАСНОСТЬ

| Файл | Git | Сервер |
|------|-----|--------|
| `.env` | ❌ В .gitignore | ✅ Только на сервере |
| `.py` код | ✅ На GitHub | ✅ `git pull` |
| Логи | ❌ В .gitignore | ✅ `/opt/agrio-bot/logs/` |

---

## ⚠️ ВАЖНО

1. **Никогда не коммитьте `.env`** — токены только на сервере!
2. **Делайте бэкап `.env`** перед `git pull`
3. **Проверяйте логи** после обновления
4. **Не редактируйте файлы на сервере** — только через Git

---

## 📞 ЕСЛИ ЧТО-ТО ПОШЛО НЕ ТАК

```bash
# 1. Проверьте статус
systemctl status agrio-bot

# 2. Посмотрите логи
journalctl -u agrio-bot -n 100 --no-pager

# 3. Проверьте .env
cat /opt/agrio-bot/.env

# 4. Перезапустите бота
systemctl restart agrio-bot

# 5. Откат к предыдущей версии
cd /opt/agrio-bot
git log --oneline -5  # Найти последний рабочий коммит
git reset --hard <commit-hash>
systemctl restart agrio-bot
```
