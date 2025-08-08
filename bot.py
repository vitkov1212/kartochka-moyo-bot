import os
import json
import gspread
import asyncio
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

# Flask для открытия порта
from flask import Flask
from threading import Thread

# Telegram
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "7620145899"
bot = Bot(token=TELEGRAM_TOKEN)

# Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1PCyseZFzE_FO51DMcp5hqOlJkqCfW7aNirWc8wuTftA").worksheet("Reports")

# Задачи
tasks = [
    {"time": "17:00", "range": "B3:D7"},
    {"time": "18:00", "range": "F3:H7"},
    {"time": "19:00", "range": "K3:M7"},
    {"time": "20:00", "range": "O3:Q7"},
    {"time": "21:00", "range": "B10:D14"},
    {"time": "22:00", "range": "F10:H14"},
    {"time": "23:00", "range": "K10:M14"},
    {"time": "00:00", "range": "O10:Q14"},
    {"time": "01:00", "range": "B17:D21"},
    {"time": "02:00", "range": "F17:H21"},
    {"time": "03:00", "range": "K17:M21"},
    {"time": "04:00", "range": "O17:Q21"},
    {"time": "05:00", "range": "B24:D28"},
    {"time": "06:00", "range": "F24:H28"},
    {"time": "07:00", "range": "K24:M28"},
    {"time": "10:00", "range": "B38:D42"},
    {"time": "11:00", "range": "F38:H42"},
    {"time": "12:00", "range": "K38:M42"},
    {"time": "13:00", "range": "B46:D50"},
    {"time": "14:00", "range": "F46:H50"},
    {"time": "15:00", "range": "K46:M50"},
    {"time": "16:00", "range": "O46:Q50"},
]

# Асинхронная отправка
async def send_report_async(cell_range):
    data = sheet.get(cell_range)
    report = "\n".join(["\t".join(row) for row in data])
    await bot.send_message(chat_id=CHAT_ID, text=f"Отчёт {cell_range}:\n{report}")

# Обёртка для APScheduler
def send_report(cell_range):
    asyncio.run(send_report_async(cell_range))

# Планировщик
scheduler = BlockingScheduler()
for task in tasks:
    hour, minute = map(int, task["time"].split(":"))
    scheduler.add_job(send_report, "cron", hour=hour, minute=minute, args=[task["range"]])

# Flask-сервер (для Render Free)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running."

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# Запуск
if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("Бот запущен...")
    scheduler.start()
