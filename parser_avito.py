import asyncio
import logging

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests
from bs4 import BeautifulSoup

url = f"https://www.avito.ru/izhevsk?q=диван&s=1"
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
    all_link = bs.find_all("div", {"class": "iva-item-priceStep-uq2CQ"})
    a = bs.find_all("h3", {"class": "styles-module-root-TWVKW"})

    price = []
    name = []

    for el in all_link:
        b = "".join(c for c in el.text if c.isdigit())
        if el.text.lower() in "цена не указана" or el.text.lower() in "бесплатно" or el.text.lower() in "цена договорная":
            price.append(0)
        else:
            price.append(f"{int(b)}")
    print(price)
    print(len(price))
    for el in a:
        if "Фильтры" not in el.text:
            name.append(f"{el.text}")
    print(name)
    print(len(name))

    info = {'Цена': price, 'Название': name}
    data = pd.DataFrame(info)

    answer = ""
    if 0 in price:
        answer += "⚠Предупреждение! Чаще всего товары с ценой 0 плохие по качеству или же имеют договорную цену!⚠"
        
    await message.answer(f"{data} {answer}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
