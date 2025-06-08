import asyncio
from aiogram import Router, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pathlib import Path
import json
import logging
from transformers import pipeline
import torch
from typing import Dict, Optional
from config import Config
from handlers.keyboards import get_navigation_buttons

router = Router()

# --- Инициализация ---
logger = logging.getLogger(__name__)

# Загрузка данных программ
def load_programs():
    try:
        with open(Path(__file__).parent.parent / "data" / "programs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки programs.json: {e}")
        return {}

programs = load_programs()

# --- Кэш выбора пользователей ---
user_selections: Dict[int, Dict] = {}  # {user_id: {"program": name, "questions_count": int}}

# --- Клавиатуры ---
def get_programs_keyboard():
    builder = ReplyKeyboardBuilder()
    for program in programs.keys():
        builder.add(types.KeyboardButton(text=program))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# --- Ленивая загрузка модели ---
_qa_model = None

def get_llm():
    global _qa_model
    if _qa_model is None:
        try:
            _qa_model = pipeline(
                "question-answering",
                model=Config.MODEL_NAME,
                device="cuda" if torch.cuda.is_available() else "cpu",
                torch_dtype=torch.float16 if torch.cuda.is_available() else None
            )
            logger.info("LLM модель инициализирована")
        except Exception as e:
            logger.error(f"Ошибка загрузки LLM: {e}")
    return _qa_model

# --- Улучшенная генерация ответов ---
async def generate_llm_answer(question: str, program_name: str) -> Optional[str]:
    try:
        context = programs[program_name].get("llm_context", "")
        if not context:
            return None
            
        # Улучшенный промпт
        result = get_llm()(
            question=f"Ответь на вопрос максимально точно и кратко (1-2 предложения), используя только данные ниже. "
                     f"Если ответа нет в данных, скажи 'Не нашел информации в данных о программе'. "
                     f"Вопрос: {question}",
            context=context,
            max_answer_len=200
        )
        
        answer = result["answer"].strip()
        
        # Фильтрация некорректных ответов
        if not answer or answer.lower() in ["нет информации", "не знаю"]:
            return None
            
        if not answer.endswith((".", "!", "?")):
            answer += "."
            
        return answer.capitalize()
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return None

def get_program_info(program_name: str) -> str:
    data = programs[program_name]
    return (
        f"🎓 <b>{program_name}</b>\n\n"
        f"▪ Бюджетные места: {data['places']['budget']} (балл: {data['passing_score']['budget']})\n"
        f"▪ Платные места: {data['places']['paid']} (балл: {data['passing_score']['paid']})\n"
        f"▪ Стоимость: {data['tuition_fee']:,} руб/год\n\n"
        f"🔗 Подробнее: {data.get('url', 'не указана')}"
    ).replace(",", " ")

# --- Обработчики сообщений ---
@router.message(lambda message: message.text == "🎓 Направления ИВМИиТ")
async def handle_programs_list(message: types.Message):
    await message.answer(
        "Выберите интересующее направление:",
        reply_markup=get_programs_keyboard()
    )

@router.message(lambda message: message.text in programs.keys())
async def handle_program_selection(message: types.Message):
    program_name = message.text
    user_selections[message.from_user.id] = {
        "program": program_name,
        "questions_count": 0
    }
    
    temp_msg = await message.answer(
        "Загружаю информацию...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await asyncio.sleep(0.5)
    await temp_msg.delete()
    
    await message.answer(
        f"Вы выбрали <b>{program_name}</b>. Можете задавать вопросы о программе.\n\n"
        "Примеры вопросов:\n"
        "• Количество бюджетных мест?\n"
        "• Сколько стоит обучение?\n"
        "• Какие дисциплины изучают?\n\n"
        "Чтобы закончить, нажмите 'В главное меню'",
        reply_markup=get_navigation_buttons(),
        parse_mode="HTML"
    )

@router.message(lambda message: message.from_user.id in user_selections)
async def handle_program_question(message: types.Message):
    user_data = user_selections[message.from_user.id]
    program_name = user_data["program"]
    user_data["questions_count"] += 1
    
    llm_answer = await generate_llm_answer(message.text, program_name)
    
    if llm_answer:
        response = f"<b>{program_name}</b>\n\n{llm_answer}"
    else:
        response = (f"По вашему вопросу не найдено информации в данных о программе.\n"
                   f"Вот основная информация о программе:\n\n"
                   f"{get_program_info(program_name)}")
    
    await message.answer(
        response,
        reply_markup=get_navigation_buttons(),
        parse_mode="HTML"
    )
