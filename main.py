import requests
import aiogram
from bs4 import BeautifulSoup

TOKEN = "6695140646:AAGSRVGWqW6Y-FULUJ2cXqs7Vpa21ZCq9E4"
html = requests.get("https://www.sports.ru/football/news/").text
soup = BeautifulSoup(html)

print(soup.find_all('title'))
vid = []
for el in soup.find_all("div", {"class": "news"}):
    for j in el.find_all('a', href=True):
        if 'Реклама на Sports.ru' not in j:
            vid.append(j.text)
    print('$')
print(vid)

d = {
    soup.find("div", {"class": "short-news"})
}
