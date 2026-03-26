# 📦 Деплой Agrio бота на сервер Proxmox

## 📋 Требования

1. Доступ к серверу Proxmox по SSH
2. Установленный Python 3.8+ на сервере
3. Установленные `rsync` и `scp` на локальной машине

## 🚀 Быстрый старт

### 1. Подготовка

Проверьте, что `.env` файл содержит правильные данные:

```bash
# Проверьте файл .env
BOT_TOKEN=ваш_токен_бота
YANDEX_API_KEY=ваш_ключ_Yandex
YANDEX_FOLDER_ID=ваш_folder_ID
ADMIN_ID=ваш_telegram_id
ALLOWED_CHAT_IDS=разрешённые_chat_id
```

### 2. Деплой

**Windows (PowerShell):**
```powershell
bash deploy.sh root@<IP_сервера>
```

**Пример:**
```powershell
bash deploy.sh root@192.168.1.100
```

### 3. Проверка

После деплоя проверьте работу бота:

```powershell
# Проверка статуса
ssh root@<IP_сервера> "systemctl status agrio-bot"

# Просмотр логов
ssh root@<IP_сервера> "journalctl -u agrio-bot -f"
```

## 🔧 Управление ботом на сервере

| Команда | Описание |
|---------|----------|
| `systemctl start agrio-bot` | Запустить бота |
| `systemctl stop agrio-bot` | Остановить бота |
| `systemctl restart agrio-bot` | Перезапустить бота |
| `systemctl status agrio-bot` | Проверить статус |
| `journalctl -u agrio-bot -f` | Смотреть логи в реальном времени |

## 📦 Бэкап

Перед обновлением создайте бэкап:

```powershell
bash backup.sh root@<IP_сервера>
```

Бэкапы хранятся в `/opt/backups/agrio-bot/`

### Восстановление из бэкапа

```bash
# На сервере
cd /opt/backups/agrio-bot
tar -xzf agrio-bot.backup.YYYYMMDD_HHMMSS.tar.gz -C /opt/
systemctl restart agrio-bot
```

## 🛠️ Структура на сервере

```
/opt/agrio-bot/
├── main.py              # Основной файл бота
├── config.py            # Конфигурация
├── ai_service.py        # ИИ сервис
├── moderation.py        # Модерация
├── seeds_database.py    # База семян
├── prompts.py           # Промпты для ИИ
├── logger.py            # Логгер
├── requirements.txt     # Зависимости
├── .env                 # Переменные окружения (600 права)
├── venv/                # Виртуальное окружение
├── logs/                # Логи бота
└── start.bat            # (не используется на Linux)

/etc/systemd/system/agrio-bot.service  # Systemd сервис
/opt/backups/agrio-bot/                # Бэкапы
```

## 🔐 Безопасность

- `.env` файл копируется с правами `600` (только чтение владельцем)
- Скрипт использует `rsync` для безопасной передачи файлов
- Бэкапы автоматически удаляются (хранятся последние 5)

## ⚠️ Важные замечания

1. **Не редактируйте файлы на сервере вручную** — вносите изменения локально и делайте деплой
2. **Всегда делайте бэкап** перед деплоем
3. **Проверяйте логи** после деплоя
4. **Не коммитьте `.env`** в Git — он копируется отдельно

## 🐛 Отладка

Если бот не работает:

1. Проверьте логи:
   ```bash
   ssh root@<IP> "journalctl -u agrio-bot -n 50 --no-pager"
   ```

2. Проверьте, что сервис запущен:
   ```bash
   ssh root@<IP> "systemctl status agrio-bot"
   ```

3. Перезапустите бота:
   ```bash
   ssh root@<IP> "systemctl restart agrio-bot"
   ```

4. Проверьте `.env` файл:
   ```bash
   ssh root@<IP> "cat /opt/agrio-bot/.env"
   ```

## 📞 Поддержка

При проблемах:
1. Создайте бэкап
2. Проверьте логи
3. Перезапустите бота
4. При необходимости — восстановите из бэкапа
