import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio

TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Этот бот будет принимать PDF и Excel с кодами. 🚀")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
