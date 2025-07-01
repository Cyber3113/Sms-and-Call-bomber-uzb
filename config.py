import os
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# SMS API URLs
SMS_API_URL1 = os.getenv("SMS_API_URL1")
SMS_API_URL2 = os.getenv("SMS_API_URL2")
SMS_API_URL5 = os.getenv("SMS_API_URL5")
SMS_API_URL6 = os.getenv("SMS_API_URL6")
SMS_API_URL7 = os.getenv("SMS_API_URL7")

CALL_API_URL1 = os.getenv("CALL_API_URL1")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
