# 🚀 БЫСТРАЯ ОЧИСТКА СЕРВЕРА

**Дата:** 31 марта 2026

---

## ⚡ Быстрые команды (копировать и вставить)

### 1. Подключение
```bash
ssh root@93.84.121.179
# Пароль: 79599687959968!
```

### 2. Всё в одном (скопировать весь блок)
```bash
# Остановка Ollama
systemctl stop ollama
systemctl disable ollama

# Удаление Ollama и моделей
rm -f /usr/local/bin/ollama
rm -rf /usr/share/ollama
rm -rf ~/.ollama
rm -f /etc/systemd/system/ollama.service
systemctl daemon-reload

# Обновление бота
cd /opt/agrio-bot
cp .env .env.backup
git pull origin main

# Удаление лишних файлов
rm -f test_ollama.py
rm -f INSTALL_LOCAL_QWEN.md
rm -f LOCAL_QWEN.md
rm -f QWEN_SETUP.md

# Перезапуск бота
systemctl restart agrio-bot

# Проверка
systemctl status agrio-bot --no-pager
echo "---"
df -h /
echo "---"
du -sh /opt/agrio-bot
```

---

## ✅ Проверка в Telegram

1. `/start` - бот отвечает
2. `Каталог` - показывает все семена
3. `Когда сажать томаты?` - отвечает из базы знаний

---

## 📊 Освобождено места

```bash
# До очистки
df -h /

# После очистки
df -h /
```

**Ожидаемое освобождение:** ~5-14 GB

---

## 🆘 Если проблема

```bash
# Проверка логов
journalctl -u agrio-bot -n 30 --no-pager

# Проверка .env
cat /opt/agrio-bot/.env

# Ручной запуск для проверки
cd /opt/agrio-bot
source venv/bin/activate
python main.py
# Нажать Ctrl+C и перезапустить через systemctl
systemctl start agrio-bot
```
