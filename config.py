import os
from dotenv import load_dotenv
import telebot


# تحميل المتغيرات من ملف .env
load_dotenv()

# إعدادات البوت
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
urlacc = "https://t.me/SAP1O"
bot = telebot.TeleBot(TOKEN)
sub_channels = ["@hx5cb", "@NVLS1O"]

# إعدادات قاعدة البيانات
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
