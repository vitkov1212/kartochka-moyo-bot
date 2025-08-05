import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

TELEGRAM_TOKEN = "8213396742:AAE_to8kw0xyMXulWquPRtSLEiepC9lyBq0"
CHAT_ID = "7620145809"  # твой chat_id

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/service_account.json", scope)
client = gspread.authorize(creds)

SPREADSHEET_NAME = "MOYO ONLINE VIP CARDS 2"
WORKSHEET_NAME = "Reports"

sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
bot = Bot(token=TELEGRAM_TOKEN)

def send_hourly_report():
    now = datetime.datetime.now()
    current_hour = now.strftime("%H:00")
    next_hour = (now + datetime.timedelta(hours=1)).strftime("%H:00")
    time_range = f"{current_hour} - {next_hour}"

    data = sheet.get_all_values()

    report = ""
    for i, row in enumerate(data):
        if time_range in row:
            for r in data[i+1:i+5]:
                if len(r) >= 2:
                    report += f"{r[0]}: {r[1]}\n"
            break

    if report:
        bot.send_message(CHAT_ID, f"Отчёт за {time_range}:\n{report}")

scheduler = BlockingScheduler()
scheduler.add_job(send_hourly_report, 'cron', minute=0)

scheduler.start()


