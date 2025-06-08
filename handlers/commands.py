from aiogram import Router, types
from aiogram.filters import Command

from handlers.keyboards import get_main_keyboard, get_navigation_buttons

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        get_start_message(),
        reply_markup=get_main_keyboard()
    )
    
def get_start_message():
    return (
        "<b>✨ Привет, абитуриент! ✨</b>\n\n"
        "Я помогу тебе с поступлением в <i>Казанский федеральный университет</i> (КФУ).\n\n"
        "<b>📌 Выбери вопрос:</b>\n"
        "✅ <b>«Приёмная комиссия КФУ»</b> – всё о документах, экзаменах и сроках.\n"
        "✅ <b>«Направления ИВМИиТ»</b> – список программ Института вычислительной математики и информатики.\n\n"
        "<b>🚀 Готов к поступлению? Начинаем!</b>"
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Выбери нужный тебе раздел и задавай свой вопрос. Всё просто :) \n\nЕсли возникли трудности, пиши в поддержку @lin_27n", reply_markup=get_main_keyboard())

@router.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(
        "ℹ Информация о боте:\n\n"
        "Версия: 1.0\n"
        "Обновлено: 06.2025\n"
        "Разработчик: @lin_27n",
        reply_markup=get_navigation_buttons()
    )

@router.message(Command("programs"))
async def list_programs(message: types.Message):
    #Список всех программ
    from handlers.program_handler import programs
    
    msg = "🎓 Доступные направления:\n\n" + \
          "\n".join(f"• {p}" for p in programs.keys()) + \
          "\n\nЕсли хочешь задать вопрос о направлении, переходи в Главное меню, а оттуда <b>«Направления ИВМИиТ»</b>"
    
    await message.answer(msg)