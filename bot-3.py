import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from anthropic import Anthropic

# Включи логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Замени на свои токены
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ANTHROPIC_API_KEY = "YOUR_ANTHROPIC_API_KEY"

# Инициализируем бот и диспетчер
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Инициализируем Anthropic клиент
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Храним историю разговоров для каждого пользователя
user_conversations = {}

def get_conversation_history(user_id):
    """Получи историю разговора пользователя"""
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    return user_conversations[user_id]

async def get_claude_response(user_id, user_message):
    """Получи ответ от Claude"""
    history = get_conversation_history(user_id)
    
    # Добавляем сообщение пользователя
    history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Отправляем запрос в Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=history
        )
        
        # Получаем ответ
        assistant_message = response.content[0].text
        
        # Добавляем ответ в историю
        history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Сохраняем только последние 20 сообщений для экономии памяти
        if len(history) > 20:
            user_conversations[user_id] = history[-20:]
        
        return assistant_message
    
    except Exception as e:
        logger.error(f"Ошибка при обращении к Claude API: {e}")
        return f"Ошибка: {str(e)}"

@dp.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start"""
    await message.reply(
        "Привет! 👋\n\n"
        "Я бот, который отвечает через Claude AI.\n"
        "Просто напиши мне сообщение и я помогу!\n\n"
        "/clear - очистить историю разговора\n"
        "/help - справка"
    )

@dp.message(Command("help"))
async def help_handler(message: Message):
    """Обработчик команды /help"""
    await message.reply(
        "Как использовать бота:\n\n"
        "1️⃣ Напиши любой вопрос или текст\n"
        "2️⃣ Бот ответит через Claude AI\n"
        "3️⃣ История сохраняется в этой сессии\n\n"
        "Команды:\n"
        "/start - начало\n"
        "/clear - очистить историю\n"
        "/help - эта справка"
    )

@dp.message(Command("clear"))
async def clear_handler(message: Message):
    """Обработчик команды /clear"""
    user_id = message.from_user.id
    if user_id in user_conversations:
        user_conversations[user_id] = []
    await message.reply("✅ История разговора очищена!")

@dp.message()
async def message_handler(message: Message):
    """Обработчик обычных сообщений"""
    user_id = message.from_user.id
    user_text = message.text
    
    # Показываем, что бот печатает
    await bot.send_chat_action(user_id, "typing")
    
    # Получаем ответ от Claude
    response = await asyncio.to_thread(
        get_claude_response, 
        user_id, 
        user_text
    )
    
    # Отправляем ответ
    # Если ответ больше 4096 символов, разбиваем на части
    if len(response) > 4096:
        for i in range(0, len(response), 4096):
            await message.reply(response[i:i+4096])
    else:
        await message.reply(response)

async def main():
    """Главная функция"""
    logger.info("Бот запускается...")
    
    # Удаляем старые обновления
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем polling
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
