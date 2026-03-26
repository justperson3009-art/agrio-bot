# 📦 Git Деплой Agrio бота

## 📋Workflow (как у бота отчетов)

### ТЕРМИНАЛ 1: Компьютер (Windows PowerShell)
```powershell
cd "C:\Users\user\Desktop\Agrio Bot"
```

### ТЕРМИНАЛ 2: Сервер Proxmox (SSH)
```bash
ssh root@93.84.121.179
# Пароль: 79599687959968!
```

---

## 🚀 Пошаговый процесс

### ШАГ 1: Создание репозитория на GitHub

1. Откройте https://github.com/new
2. Название: `agrio-bot`
3. Видимость: Private (рекомендуется) или Public
4. **НЕ** создавайте README, .gitignore, license (репозиторий уже существует локально)
5. Нажмите "Create repository"

### ШАГ 2: Привязка удалённого репозитория (Компьютер)

```powershell
cd "C:\Users\user\Desktop\Agrio Bot"

# Замените YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/agrio-bot.git

# Или через SSH (если настроен SSH ключ GitHub):
# git remote add origin git@github.com:YOUR_USERNAME/agrio-bot.git

# Проверка
git remote -v

# Отправка на GitHub
git push -u origin main
# Или если главная ветка master:
git push -u origin master
```

### ШАГ 3: Клонирование на сервер (Сервер)

```bash
# На сервере
cd /opt
git clone https://github.com/YOUR_USERNAME/agrio-bot.git
cd agrio-bot

# Или через SSH:
# git clone git@github.com:YOUR_USERNAME/agrio-bot.git
```

### ШАГ 4: Настройка .env на сервере (Сервер)

```bash
cd /opt/agrio-bot

# Создание .env файла
nano .env

# Вставьте содержимое:
BOT_TOKEN=ваш_токен
YANDEX_API_KEY=ваш_ключ
YANDEX_FOLDER_ID=ваш_folder_id
ADMIN_ID=ваш_id
ALLOWED_CHAT_IDS=разрешённые_chat_id

# Сохраните: Ctrl+O, Enter, Exit: Ctrl+X

# Права доступа
chmod 600 .env
```

### ШАГ 5: Установка и запуск (Сервер)

```bash
cd /opt/agrio-bot

# Python виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Systemd сервис
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

# Запуск
systemctl daemon-reload
systemctl enable agrio-bot
systemctl start agrio-bot

# Проверка
systemctl status agrio-bot
journalctl -u agrio-bot -f
```

---

## 🔄 Обновление кода (после изменений)

### ТЕРМИНАЛ 1 (Компьютер):
```powershell
cd "C:\Users\user\Desktop\Agrio Bot"

# Проверка изменений
git status

# Добавление и коммит
git add -A
git commit -m "Описание изменений"

# Отправка на GitHub
git push
```

### ТЕРМИНАЛ 2 (Сервер):
```bash
cd /opt/agrio-bot

# Бэкап .env (на всякий случай)
cp .env .env.backup

# Получение обновлений
git pull origin main
# или
git pull origin master

# Перезапуск бота
systemctl restart agrio-bot

# Проверка логов
journalctl -u agrio-bot -f
```

---

## 🔐 Безопасность

| Что | Где | Git |
|-----|-----|-----|
| `.env` | Только на сервере | ❌ В .gitignore |
| Код (.py) | Компьютер + GitHub + Сервер | ✅ Коммитим |
| Логи | Только на сервере | ❌ В .gitignore |
| БД | Только на сервере | ❌ В .gitignore |

---

## 📊 Структура

```
Компьютер (C:\Users\user\Desktop\Agrio Bot)
    ↓ git push
GitHub (github.com/YOUR_USERNAME/agrio-bot)
    ↓ git clone / git pull
Сервер (/opt/agrio-bot)
```

---

## 🛠️ Полезные команды

### Git:
```powershell
git status          # Статус файлов
git log --oneline   # История коммитов
git branch          # Ветки
git remote -v       # Удалённые репозитории
```

### Server:
```bash
systemctl status agrio-bot     # Статус бота
journalctl -u agrio-bot -f     # Логи
git pull                       # Обновление кода
```

---

## ⚠️ Важно

1. **Никогда не коммитьте `.env`** — токены должны быть только на сервере
2. **Всегда делайте `git pull`** перед редактированием на сервере
3. **Проверяйте логи** после каждого обновления
4. **Создавайте бэкап** `.env` перед `git pull`
