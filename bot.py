import os
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

# Настройки
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")  # токен из переменных окружения
CHAT_ID = "7620145899"  # твой chat_id

# Google Sheets доступ через JSON из переменной окружения
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

SPREADSHEET_ID = "1PCyseZFzE_FO51DMcp5hqOlJkqCfW7aNirWc8wuTftA"
WORKSHEET_NAME = "Reports"

sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)
bot = Bot(token=TELEGRAM_TOKEN)

# Список задач: время -> диапазон ячеек
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

# Отправка диапазона
def send_report(cell_range):
    data = sheet.get(cell_range)
    report = "\n".join(["\t".join(row) for row in data])
    bot.send_message(chat_id=CHAT_ID, text=f"Отчёт {cell_range}:\n{report}")

# Планировщик
scheduler = BlockingScheduler()

for task in tasks:
    hour, minute = map(int, task["time"].split(":"))
    scheduler.add_job(send_report, "cron", hour=hour, minute=minute, args=[task["range"]])

print("Бот запущен...")
scheduler.start()
