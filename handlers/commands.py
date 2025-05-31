from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот-помощник для студентов. Задайте вопрос (например, 'проходной балл')."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Список тем: проходной балл, срок действия, уровень математики.")