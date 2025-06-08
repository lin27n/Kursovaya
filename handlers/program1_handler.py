import json
from pathlib import Path
from aiogram import Router, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import Dict

from handlers.keyboards import get_navigation_buttons

router = Router()

# Загрузка данных программ
def load_programs():
    with open(Path(__file__).parent.parent / "data" / "programs.json", "r", encoding="utf-8") as f:
        return json.load(f)

programs = load_programs()

# Кэш выбора пользователей
user_selections: Dict[int, str] = {}

# Клавиатура для выбора программ
def get_programs_keyboard():
    builder = ReplyKeyboardBuilder()
    for program in programs.keys():
        builder.add(types.KeyboardButton(text=program))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# Rule-based обработка вопросов
def process_question(question: str, program_data: Dict) -> str:
    question_lower = question.lower()
    
    # Словарь для сопоставления ключевых слов с полями данных
    rules = {
        "бюджет": ("places", "budget"),
        "платн": ("places", "paid"),
        "стоимость": ("tuition_fee",),
        "цена": ("tuition_fee",),
        "проходн": ("passing_score",),
        "балл": ("passing_score",),
        "мест": ("places",),
        "стоит": ("tuition_fee",)
    }
    
    # Определяем тип вопроса
    question_type = None
    target = None  # budget или paid
    
    for keyword, fields in rules.items():
        if keyword in question_lower:
            question_type = fields
            if "бюджет" in question_lower:
                target = "budget"
            elif "платн" in question_lower:
                target = "paid"
            break
    
    # Формируем ответ
    if question_type:
        try:
            data = program_data
            for field in question_type:
                data = data[field]
            
            if target and isinstance(data, dict):
                value = data[target]
            else:
                value = data
                
            if "passing_score" in question_type:
                return f"Проходной балл: {value}"
            elif "places" in question_type:
                return f"Количество мест: {value}"
            elif "tuition_fee" in question_type:
                return f"Стоимость обучения: {value:,} руб/год".replace(",", " ")
        except (KeyError, TypeError):
            pass
    
    # Если вопрос не распознан, возвращаем общую информацию
    return format_program_info(program_data)

# Форматирование общей информации
def format_program_info(program_data: Dict) -> str:
    return (
        f"🎓 Основная информация:\n\n"
        f"▪ Бюджетные места: {program_data['places']['budget']}\n"
        f"▪ Проходной балл (бюджет): {program_data['passing_score']['budget']}\n"
        f"▪ Платные места: {program_data['places']['paid']}\n"
        f"▪ Проходной балл (платно): {program_data['passing_score']['paid']}\n"
        f"▪ Стоимость обучения: {program_data['tuition_fee']:,} руб/год\n\n"
        f"🔗 Подробнее: {program_data.get('url', 'не указана')}"
    ).replace(",", " ")

# Обработчики сообщений
@router.message(lambda message: message.text == "🎓 Направления ИВМИиТ")
async def handle_programs_list(message: types.Message):
    await message.answer(
        "Выберите интересующее направление:",
        reply_markup=get_programs_keyboard()
    )

@router.message(lambda message: message.text in programs.keys())
async def handle_program_selection(message: types.Message):
    program_name = message.text
    user_selections[message.from_user.id] = program_name
    await message.answer(
        f"Вы выбрали <b>{program_name}</b>. Задайте вопрос о программе.\n\n"
        "Примеры вопросов:\n"
        "• Сколько бюджетных мест?\n"
        "• Какой проходной балл на платную основу?\n"
        "• Какая стоимость обучения?\n\n<b>Пишите четко и без опечаток</b>",
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

@router.message(lambda message: message.from_user.id in user_selections)
async def handle_program_question(message: types.Message):
    program_name = user_selections[message.from_user.id]
    program_data = programs[program_name]
    
    # Обрабатываем вопрос
    response = process_question(message.text, program_data)
    
    await message.answer(
        f"<b>{program_name}</b>\n\n{response}",
        parse_mode="HTML",
        reply_markup=get_navigation_buttons()
    )
