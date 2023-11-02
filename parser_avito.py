import asyncio
import logging

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests
from bs4 import BeautifulSoup

url = f"https://www.avito.ru/izhevsk?q=ssd&s=1"
html = requests.get(url).text
bs = BeautifulSoup(html)

info = {'Название': [0, 0], 'Цена': [0, 0]}
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
    global data
    global info

    all_link = bs.find_all("div", {"class": "iva-item-priceStep-uq2CQ"})
    a = bs.find_all("h3", {"class": "styles-module-root-TWVKW"})

    prices = []
    name = []

    for el in all_link:
        b = "".join(c for c in el.text if c.isdigit())
        if el.text.lower() in "цена не указана" or el.text.lower() in "бесплатно" or el.text.lower() in "цена договорная":
            prices.append(0)
        else:
            prices.append(f"{int(b)}")
    print(prices)
    print(len(prices))

    for el in a:
        if "Фильтры" not in el.text:
            name.append(f"{el.text}")

    print(name)
    print(len(name))

    info = {'Цена': prices[:5], 'Название': name[:5]}
    data = pd.DataFrame(info)


    answer = "\n"
    if 0 in prices:
        answer += "\n⚠Предупреждение! Чаще всего товары с ценой 0 плохие по качеству или же имеют договорную цену!⚠"

    await message.answer(f"{data} {answer}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
