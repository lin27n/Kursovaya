import logging
from aiogram import Bot, Dispatcher
from config import Config
from handlers import commands, messages

async def main():
    # Настройка логгирования
    logging.basicConfig(level=logging.INFO)

    # Инициализация бота
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    # Подключение обработчиков
    dp.include_router(commands.router)
    dp.include_router(messages.router)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())