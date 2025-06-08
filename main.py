import logging
from aiogram import Bot, Dispatcher, types
from config import Config
from handlers import commands, faq_handler, program_handler, program1_handler
from aiogram.client.default import DefaultBotProperties
import gc
import torch


from handlers.keyboards import get_main_keyboard

gc.collect()
torch.cuda.empty_cache() if torch.cuda.is_available() else None
async def on_startup():
    print("Бот успешно запущен...")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', mode='w'),
        logging.StreamHandler()
    ]
)
async def main():
    
    bot = Bot(
        token=Config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()
    dp.include_router(commands.router) 
    dp.include_router(program1_handler.router)  # Сначала проверяем программы
    dp.include_router(faq_handler.router)     # Затем частые вопросы

    dp.startup.register(on_startup)
    
    @dp.callback_query(lambda c: c.data in ["main_menu"])
    async def handle_navigation(callback: types.CallbackQuery):
        if callback.data == "main_menu":
            if callback.from_user.id in program1_handler.user_selections:
                del program1_handler.user_selections[callback.from_user.id]
            await callback.answer("Возвращаемся в главное меню..."),
            await asyncio.sleep(0.5),  # Пауза 500 мс
            await callback.message.answer(
                commands.get_start_message(),
                reply_markup=get_main_keyboard()
            )
        await callback.answer()
        
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.critical(f"Бот упал с ошибкой: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    