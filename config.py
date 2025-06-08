from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    MODEL_NAME = "Stacy123/rubert_tiny2_qa"