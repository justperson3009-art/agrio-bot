# 🤖 Локальная установка Qwen на сервер

## 📋 Преимущества локальной установки

| Параметр | Cloud API | Локально |
|----------|-----------|----------|
| **Стоимость** | Бесплатно (лимиты) | Бесплатно |
| **Лимиты** | Есть | Нет |
| **Скорость** | Зависит от интернета | Максимальная |
| **Приватность** | Данные у провайдера | Данные у вас |
| **Доступ** | Нужен интернет | Работает без интернета |

---

## 🔧 Требования

**Минимальные:**
- RAM: 8GB (для 7B модели)
- CPU: 4 ядра
- Место: 10GB

**Рекомендуемые:**
- RAM: 16GB+ (для 14B модели)
- GPU: NVIDIA (опционально, ускоряет в 10x)
- Место: 20GB+

---

## 📦 Установка Ollama (проще всего)

### Шаг 1: Проверка ресурсов сервера

```bash
# Оперативная память
free -h

# Место на диске
df -h /

# Количество ядер CPU
nproc

# Информация о CPU
cat /proc/cpuinfo | grep "model name" | head -1
```

### Шаг 2: Установка Ollama

```bash
# Установка Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Проверка установки
ollama --version
```

### Шаг 3: Запуск Qwen модели

```bash
# Для серверов с 8GB RAM (7B модель)
ollama run qwen2.5:7b

# Для серверов с 16GB RAM (14B модель)
ollama run qwen2.5:14b

# Для серверов с 32GB+ RAM (32B модель)
ollama run qwen2.5:32b
```

**Рекомендуемая модель:** `qwen2.5:7b` или `qwen2.5:14b`

---

## ⚙️ Настройка бота для локальной работы

### 1. Обновите ai_service.py

Измените URL для локального Ollama:

```python
def __init__(self):
    self.api_key = None  # Не нужен для локальной версии
    self.model = "qwen2.5:7b"  # Или ваша модель
    self.url = "http://localhost:11434/api/generate"
```

### 2. Обновите метод get_consultation

```python
async def get_consultation(self, user_message: str, dialog_context: List = None) -> str:
    # ... проверки ...
    
    # Формируем промпт
    prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"
    
    # Тело запроса для Ollama
    payload = {
        "model": self.model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 1500
        }
    }
    
    # Заголовки
    headers = {"Content-Type": "application/json"}
    
    try:
        session = await self._get_session()
        async with session.post(
            self.url,
            json=payload,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
        ) as response:
            result = await response.json()
            answer = result.get("response", "")
            # ... обработка ...
```

---

## 🚀 Автозапуск Ollama

### Создайте systemd сервис для Ollama

```bash
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

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ollama
systemctl start ollama
```

---

## 📊 Мониторинг

```bash
# Статус Ollama
systemctl status ollama

# Логи
journalctl -u ollama -f

# Проверка модели
ollama list

# Использование RAM
ollama ps
```

---

## 🎯 Быстрая установка (все команды сразу)

```bash
# 1. Установка Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Запуск сервиса
systemctl daemon-reload
systemctl enable ollama
systemctl start ollama

# 3. Загрузка модели (7B для 8GB RAM)
ollama pull qwen2.5:7b

# 4. Проверка
ollama run qwen2.5:7b "Привет! Как дела?"
```

---

## 📝 Обновление .env

```bash
cd /opt/agrio-bot
nano .env
```

Добавьте:
```
# Локальная Qwen модель
QWEN_LOCAL=true
QWEN_MODEL=qwen2.5:7b
OLLAMA_URL=http://localhost:11434
```

---

## ⚠️ Возможные проблемы

### Недостаточно RAM

**Решение:** Используйте меньшую модель
```bash
ollama pull qwen2.5:3b  # Для 4GB RAM
ollama pull qwen2.5:1.8b  # Для 2GB RAM
```

### Медленная генерация

**Решение:**
1. Закройте лишние процессы
2. Уменьшите размер модели
3. Добавьте GPU (если есть)

### Ollama не запускается

**Решение:**
```bash
# Проверьте логи
journalctl -u ollama -f

# Перезапустите
systemctl restart ollama
```

---

## ✅ Чеклист

- [ ] Проверены ресурсы сервера
- [ ] Ollama установлен
- [ ] Модель загружена
- [ ] Сервис запущен
- [ ] Бот обновлён
- [ ] Тестовый запрос работает

---

**Готово!** Qwen работает локально на вашем сервере! 🎉
