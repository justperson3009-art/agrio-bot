# 🚀 БЫСТРЫЙ ДЕПЛОЙ Agrio бота на сервер

## Вариант 1: SSH ключи (рекомендуется)

### Шаг 1: Генерация SSH ключа (если нет)
```powershell
ssh-keygen -t ed25519
```

### Шаг 2: Копирование ключа на сервер
```powershell
ssh-copy-id root@93.84.121.179
# Или вручную:
# type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh root@93.84.121.179 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Шаг 3: Запуск деплоя
```powershell
.\deploy.ps1
```

---

## Вариант 2: Ручной деплой (команды для выполнения)

### 1. Подключение к серверу
```powershell
ssh root@93.84.121.179
```

### 2. Создание директории
```bash
mkdir -p /opt/agrio-bot
cd /opt/agrio-bot
```

### 3. Копирование файлов (с локального компьютера)
```powershell
# В PowerShell на компьютере:
cd "C:\Users\user\Desktop\Agrio Bot"
scp -r * root@93.84.121.179:/opt/agrio-bot/
scp .env root@93.84.121.179:/opt/agrio-bot/.env
```

### 4. Настройка на сервере (выполнять на сервере)
```bash
cd /opt/agrio-bot

# Установка зависимостей
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Права на .env
chmod 600 .env

# Создание systemd сервиса
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

## Проверка работы

После деплоя проверьте бота:
1. Откройте Telegram
2. Найдите бота по токену из `.env`
3. Нажмите `/start`
4. Бот должен ответить

---

## Логи

```bash
# Просмотр логов в реальном времени
journalctl -u agrio-bot -f

# Последние 50 строк
journalctl -u agrio-bot -n 50 --no-pager
```

---

## Управление

```bash
systemctl start agrio-bot      # Запустить
systemctl stop agrio-bot       # Остановить
systemctl restart agrio-bot    # Перезапустить
systemctl status agrio-bot     # Статус
```
