import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

# Настройки
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")  # токен берем из переменных окружения
CHAT_ID = "7620145899"  # твой chat_id

# Google Sheets доступ
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/service_account.json", scope)
client = gspread.authorize(creds)

SPREADSHEET_NAME = "MOYO ONLINE VIP CARDS 2"
WORKSHEET_NAME = "Reports"

sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
bot = Bot(token=TELEGRAM_TOKEN)

# Список задач: время -> диапазон ячеек
tasks = [
    {"time": "17:00", "range": "B3:D7"},   # 16:00–17:00
    {"time": "18:00", "range": "F3:H7"},   # 17:00–18:00
    {"time": "19:00", "range": "K3:M7"},   # 18:00–19:00
    {"time": "20:00", "range": "O3:Q7"},   # 19:00–20:00
    {"time": "21:00", "range": "B10:D14"}, # 20:00–21:00
    {"time": "22:00", "range": "F10:H14"}, # 21:00–22:00
    {"time": "23:00", "range": "K10:M14"}, # 22:00–23:00
    {"time": "00:00", "range": "O10:Q14"}, # 23:00–00:00
    {"time": "01:00", "range": "B17:D21"}, # 00:00–01:00
    {"time": "02:00", "range": "F17:H21"}, # 01:00–02:00
    {"time": "03:00", "range": "K17:M21"}, # 02:00–03:00
    {"time": "04:00", "range": "O17:Q21"}, # 03:00–04:00
    {"time": "05:00", "range": "B24:D28"}, # 04:00–05:00
    {"time": "06:00", "range": "F24:H28"}, # 05:00–06:00
    {"time": "07:00", "range": "K24:M28"}, # 06:00–07:00
    {"time": "10:00", "range": "B38:D42"}, # 09:00–10:00
    {"time": "11:00", "range": "F38:H42"}, # 10:00–11:00
    {"time": "12:00", "range": "K38:M42"}, # 11:00–12:00
    {"time": "13:00", "range": "B46:D50"}, # 12:00–13:00
    {"time": "14:00", "range": "F46:H50"}, # 13:00–14:00
    {"time": "15:00", "range": "K46:M50"}, # 14:00–15:00
    {"time": "16:00", "range": "O46:Q50"}, # 15:00–16:00
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

