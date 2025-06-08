# -*- coding: utf-8 -*-
import json
import logging
from aiogram import Router, types
from pathlib import Path
from difflib import SequenceMatcher

from handlers.keyboards import get_navigation_buttons

router = Router()

KFU_KEYWORDS = [
    "кфу", "казан", "универ", "поступ", "бюджет", "общежит", 
    "документ", "факультет", "специальност", "егэ", "вступительн",
    "приемн", "балл", "зачисл", "магистратур", "бакалавриат", "проходн"
]

@router.message(lambda message: message.text == "❓ Приемная комиссия КФУ")
async def handle_admission(message: types.Message):
    await message.answer(
        "Задайте вопрос о документах, сроках подачи или других общих вопросах:",
        reply_markup=types.ReplyKeyboardRemove(),
    )

# Загрузка жестких правил
try:
    with open(Path(__file__).parent.parent / "data" / "faq.json", "r", encoding="utf-8") as f:
        hard_rules = json.load(f)
    logging.info("Правила успешно загружены")
except Exception as e:
    logging.error(f"Ошибка загрузки правил: {e}")
    hard_rules = {}

def find_best_match(user_text: str, threshold: float = 0.65) -> dict:
    #Находит наиболее подходящий вопрос в базе
    user_text = user_text.lower().strip()
    best_match = None
    best_score = 0
    
    for topic in hard_rules["topics"]:
        # Проверяем основную фразу
        score = SequenceMatcher(None, user_text, topic["main_question"]).ratio()
        
        # Проверяем синонимы
        for synonym in topic["synonyms"]:
            current_score = SequenceMatcher(None, user_text, synonym).ratio()
            if current_score > score:
                score = current_score
                
        if score > best_score and score >= threshold:
            best_score = score
            best_match = topic
    
    return best_match

def format_response(topic: dict) -> str:
    #Форматирует ответ с ссылками
    response = topic["answer"]
    if "links" in topic:
        response += "\n\n🔗 " + "\n".join(
            f" {link['text']}: {link['url']}" for link in topic["links"]
        )
    return response

def is_about_kfu(text: str) -> bool:
    #Проверяет, относится ли вопрос к КФУ
    text = text.lower()
    return any(keyword in text for keyword in KFU_KEYWORDS)

@router.message()
async def handle_text(message: types.Message):

    if not message.text:
        await message.answer("Пожалуйста, задайте текстовый вопрос.")
        return

    user_text = message.text.lower()

    # 1. Проверка тематики
    if not is_about_kfu(user_text):
        await message.answer("Я отвечаю только на вопросы о КФУ. Задайте вопрос об университете.")
        return

    # 2. Поиск в жестких правилах
    matched_topic = find_best_match(user_text)
    
    if matched_topic:
        try:
            response = format_response(matched_topic)
            await message.answer(response, reply_markup=get_navigation_buttons())
        except Exception as e:
            logging.error(f"Ошибка форматирования ответа: {str(e)}")
            fallback_msg = matched_topic.get("answer", "Пожалуйста, уточните информацию на сайте: https://kpfu.ru")
            await message.answer(fallback_msg, reply_markup=get_navigation_buttons())
    else:
        logging.info(f"Вопрос не найден в FAQ: {user_text}")
        # Стандартный ответ с ссылкой для вопросов вне FAQ
        await message.answer(
            "Ответ на ваш вопрос не найден в базе. Пожалуйста, обратитесь напрямую:\n\n"
            "🔗 Задать вопрос приемной комиссии: https://admissions.kpfu.ru/bakalavriat-specialitet/obratnaya-svyaz/zadat-vopros/\n"
            "🔗 Официальный сайт КФУ: https://kpfu.ru",
            reply_markup=get_navigation_buttons()
        )