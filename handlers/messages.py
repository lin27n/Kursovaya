import json
import logging
from aiogram import Router, types
from openai import AsyncOpenAI
from pathlib import Path

router = Router()

# Загрузка жестких правил
with open(Path(__file__).parent.parent / "data" / "rules.json", "r", encoding="utf-8") as f:
    hard_rules = json.load(f)

# Клиент OpenAI
client = AsyncOpenAI(api_key="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")

@router.message()
async def handle_text(message: types.Message):
    user_text = message.text.lower()

    # Проверка жестких правил
    if user_text in hard_rules:
        await message.answer(hard_rules[user_text])
        return

    # Запрос к GPT
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        await message.answer("Ошибка обработки запроса. Попробуйте позже.")
        logging.error(f"OpenAI error: {e}")