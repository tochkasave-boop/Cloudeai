# 🤖 Telegram бот с Claude AI

Бот отвечает на все сообщения используя Claude AI!

## 🔧 Установка

### 1️⃣ Установи зависимости
```bash
pip install -r requirements.txt
```

### 2️⃣ Получи токены

**Telegram Bot Token:**
- Напиши @BotFather в Telegram
- Используй команду `/newbot`
- Скопируй полученный токен

**Anthropic API Key:**
- Перейди на https://console.anthropic.com
- Создай API ключ в разделе "API Keys"

### 3️⃣ Настрой конфиг

**Вариант 1: С .env файлом (безопаснее)**
```bash
# Скопируй файл
cp .env.example .env

# Отредактируй .env и добавь свои токены
TELEGRAM_BOT_TOKEN=your_token_here
ANTHROPIC_API_KEY=your_key_here

# Запусти бота
python bot_with_env.py
```

**Вариант 2: Прямо в коде**
- Открой `bot.py`
- Замени `YOUR_TELEGRAM_BOT_TOKEN` на реальный токен
- Замени `YOUR_ANTHROPIC_API_KEY` на реальный ключ
- Запусти: `python bot.py`

## 🚀 Запуск

```bash
python bot_with_env.py
```

Бот должен вывести логи типа:
```
INFO:root:🚀 Бот запускается...
```

## 💬 Команды бота

- `/start` - приветствие и помощь
- `/help` - справка
- `/clear` - очистить историю разговора

## ⚙️ Возможности

✅ Сохранение истории разговора (20 последних сообщений)
✅ Отправка "печатает..." при обработке
✅ Автоматическое разбиение длинных ответов
✅ Отдельные сессии для каждого пользователя
✅ Обработка ошибок API

## 🔒 Безопасность

⚠️ **НИКОГДА не коммитьте .env файл!**

Добавь в `.gitignore`:
```
.env
*.pyc
__pycache__/
```

## 📦 Деплой на Railway

1. Создай Procfile:
```
web: python bot_with_env.py
```

2. Добавь переменные окружения в Railway:
   - TELEGRAM_BOT_TOKEN
   - ANTHROPIC_API_KEY

3. Задеплой на Railway

## 🐛 Решение проблем

**"Ошибка при обращении к Claude API"**
- Проверь что ANTHROPIC_API_KEY правильный
- Проверь что у тебя есть баланс на Anthropic

**"Бот не отвечает"**
- Проверь TELEGRAM_BOT_TOKEN в BotFather
- Убедись что скрипт запущен

**"ModuleNotFoundError"**
- Переустанови зависимости: `pip install -r requirements.txt`
