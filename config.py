from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")