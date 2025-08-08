import os
import json
import gspread
import asyncio
import logging
from flask import Flask
from threading import Thread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime  # ← вот нужный импорт

# Логирование
logging.basicConfig(level=logging.INFO)

# Telegram
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "-1002852666984"
bot = Bot(token=TELEGRAM_TOKEN)

# Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1PCyseZFzE_FO51DMcp5hqOlJkqCfW7aNirWc8wuTftA").worksheet("Reports")

# Асинхронная отправка
async def send_report_async(cell_range):
    try:
        data = sheet.get(cell_range)
        report = "\n".join(["\t".join(row) for row in data])
        await bot.send_message(chat_id=CHAT_ID, text=f"📝 Отчёт :\n{report}")
    except Exception as e:
        logging.error(f"Ошибка при отправке отчета {cell_range}: {e}")

# Обёртка для планировщика
def send_report(cell_range):
    print(f"📤 Отправка отчёта запущена в {datetime.now()}")
    print(f"⏰ Время задачи! Отправка диапазона: {cell_range}")
    asyncio.run_coroutine_threadsafe(send_report_async(cell_range), loop)

# Задачи
tasks = [
    {"time": "13:00", "range": "С5:D9"},
    {"time": "14:00", "range": "G5:H9"},
    {"time": "15:00", "range": "K5:L9"},
    {"time": "16:00", "range": "O5:P9"},
    {"time": "17:00", "range": "C11:D15"},
    {"time": "18:00", "range": "G11:H15"},
    {"time": "19:00", "range": "K11:L15"},
    {"time": "20:00", "range": "O11:P15"},
    {"time": "21:00", "range": "C17:D21"},
    {"time": "22:00", "range": "G17:H21"},
    {"time": "23:00", "range": "K17:L21"},
    {"time": "00:00", "range": "O17:P21"},
    {"time": "01:00", "range": "B23:D27"},
    {"time": "02:00", "range": "G23:H27"},
    {"time": "03:00", "range": "K23:L27"},
    {"time": "07:00", "range": "B39:D43"},
    {"time": "08:00", "range": "G39:H43"},
    {"time": "09:00", "range": "K39:L43"},
    {"time": "10:00", "range": "C47:D51"},
    {"time": "11:00", "range": "G47:H51"},
    {"time": "12:00", "range": "K47:L51"}   
]

# Flask сервер (для Render)
app = Flask(__name__)
@app.route('/')
def home():
    return "🤖 Бот работает."

# Фоновый запуск Flask
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Запуск
if __name__ == "__main__":
    logging.info(f"🕒 Серверное время при запуске: {datetime.now()}")

    # Запуск Flask
    Thread(target=run_flask).start()

    # Асинхронный event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Планировщик
    scheduler = BackgroundScheduler()
    for task in tasks:
        hour, minute = map(int, task["time"].split(":"))
        scheduler.add_job(send_report, "cron", hour=hour, minute=minute, args=[task["range"]])
    scheduler.start()

    logging.info("✅ Бот запущен.")
    loop.run_forever()










