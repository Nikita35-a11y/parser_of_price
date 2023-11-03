import asyncio
import logging

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
import requests
from bs4 import BeautifulSoup

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6695140646:AAGSRVGWqW6Y-FULUJ2cXqs7Vpa21ZCq9E4")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="/start")],
        [types.KeyboardButton(text="/end")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer("Привет!\n Я Slice, бот для быстрого поиска бу,\n а также товаров по низким ценам 🤖")
    await message.answer("Напиши название товара или услуги 🛒", reply_markup=keyboard)


@dp.message(Command("end"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="/end")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("До встречи!\nРад был помочь 😉", reply_markup=keyboard)


@dp.message()
async def get_info(message: types.Message):
    if message.text != "" or message.text != " ":
        url_avito = f"https://www.avito.ru/all?q={message.text}&s=1"
        html = requests.get(url_avito).text
        bs = BeautifulSoup(html)

        ebay = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={message.text}&_sacat=0&_sop=15"
        html_ebay = requests.get(ebay).text
        bs_ebay = BeautifulSoup(html_ebay)

        info_ebay = {"Цена💸": [0, 0], "Название📋": [0, 0]}
        pd_ebay = pd.DataFrame(info_ebay)

        info_avito = {'Цена💸': [0, 0], 'Название📋': [0, 0]}
        data_avito = pd.DataFrame(info_avito)

        all_link = bs.find_all("div", {"class": "iva-item-priceStep-uq2CQ"})
        a = bs.find_all("h3", {"class": "styles-module-root-TWVKW"})

        n = bs_ebay.find_all("div", {"class": "s-item__title"})
        pc = bs_ebay.find_all("span", {"class": "s-item__price"})

        prices_avito = []
        names_avito = []

        names_ebay = []
        prices_ebay = []

        for el2 in n:
            names_ebay.append(el2.text)
            print(el2.text)

        for el2 in pc:
            k = "".join(c2 for c2 in el2.text if c2.isdigit())
            print(k)
            prices_ebay.append(f"{int(k)}")

        for el in all_link:
            b = "".join(c for c in el.text if c.isdigit())
            if el.text.lower() in "цена не указана" or el.text.lower() in "бесплатно" or el.text.lower() in "цена договорная":
                prices_avito.append(0)
            else:
                prices_avito.append(f"{b}")

        print(prices_avito)
        print(len(prices_avito))

        for el in a:
            if "Фильтры" not in el.text:
                names_avito.append(f"{el.text}")

        print(names_avito)
        print(len(names_avito))

        info_avito = {'Цена 💸': prices_avito[:5], 'Название 📋': names_avito[:5]}
        data_avito = pd.DataFrame(info_avito)

        info_ebay = {"Цена💸": prices_ebay[:5], "Название📋": names_ebay[:5]}
        pd_ebay = pd.DataFrame(info_ebay)

        answer = "\n"
        if 0 in prices_avito:
            answer += "\n⚠Предупреждение! Чаще всего товары с ценой 0 плохие по качеству или же имеют договорную цену!⚠"

        await message.answer(f"{data_avito} {answer}\n")
        await message.answer(f"{pd_ebay} {answer}")
    else:
        await message.answer("⚠Неверное имя товара!⚠")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
