import asyncio
import logging

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests
from bs4 import BeautifulSoup

html = requests.get("https://www.avito.ru/izhevsk?q=ssd&s=1").text
soup = BeautifulSoup(html)

info = {'Название': [1, 2], 'Цена': [1, 22]}
data = pd.DataFrame(info)
print(data)

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6695140646:AAGSRVGWqW6Y-FULUJ2cXqs7Vpa21ZCq9E4")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message(Command("info"))
async def get_info(message: types.Message):
    price = []
    name = []

    for el in soup.find_all("strong", {"class": "styles-module-root-LIAav"}):
        if el.text.lower() in "цена не указана" or el.text.lower() in "бесплатно" or el.text.lower() in "цена договорная":
            price.append(0)
        else:
            price.append(el.text.replace("0₽", ''))
    print(price[10:])
    print(len(price))
    for el in soup.find_all("h3", {"itemprop": "name"}):
        name.append(el.text)
    print(len(name))
    info = {'Цена': price[10:], 'Название': name}

    data = pd.DataFrame(info)
    print(data)
    await message.answer(f"Авито")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
