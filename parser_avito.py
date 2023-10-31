import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests
from bs4 import BeautifulSoup

html = requests.get("https://www.avito.ru/izhevsk?q=ssd").text
soup = BeautifulSoup(html)
info = []

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6695140646:AAGSRVGWqW6Y-FULUJ2cXqs7Vpa21ZCq9E4")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message(Command("price"))
async def get_price(message: types.Message):
    for el in soup.find_all("div", {"class": "items-items-kAJAg"}):
        info.append(el)
        print(info)
    await message.answer("Price")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
