import time
from threading import Thread
import requests
from lxml import html

import sqlite3

# получение данных из таблицы
def get_all_cars():
    connect = sqlite3.connect('cars_database.db')
    cursor = connect.cursor()
    get = f'SELECT * FROM cars'
    cursor.execute(get)
    result = cursor.fetchall()
    print(result , ' - Вывод')
    cursor.close()

def create_cars_db():
    # подключение к базе
    connect = sqlite3.connect('cars_database.db')
    cursor = connect.cursor()
    cursor.execute(
        '''CREATE TABLE if not exists cars (
                   model text,
                   price text
                   );'''
    )
    connect.commit()


def insert_car(car: dict):
    connect = sqlite3.connect('cars_database.db')
    cursor = connect.cursor()
    request_in_db = f'INSERT INTO cars (model, price) VALUES ("{car["model"]}", "{str(car["price"])}");'
    # print(request_in_db)
    cursor.execute(request_in_db)
    connect.commit()

def carsdata():
    url = f'https://auto.ria.com/legkovie/?page='
    for i in range(1, 11):
        response = requests.get(url + str(i))
        index = 1
        if response.status_code == 200:
            tree = html.fromstring(response.text)
            names = []
            prices = []
            for idx in range(1, 11):
                nPath = f'//*[@id="searchResults"]/section[{index}]/div[4]/div[2]/div[1]/div/a/span/text()'
                xPath = f'//*[@id="searchResults"]/section[{index}]/div[4]/div[2]/div[2]/span/span[1]/text()'
                name = tree.xpath(nPath)
                price = tree.xpath(xPath)
                if (len(name) > 0):
                    names.append(name[0])
                    prices.append(price[0])
                else:
                    print(name, price)
                index += 1
            for idx in range(len(prices)):
                # print(f'{str(idx + 1)}: {names[idx]}, price:{prices[idx]}$')
                insert_car({"model": names[idx], "price": prices[idx]})


# create_cars_db()
# start = time.perf_counter()
# for i in range(1):
#     th = Thread(target=carsdata, args=())
#     th.start()
#     end = time.perf_counter()
#     print(f'time with threads = {end - start:0.2f}')
#     print(f'working time = {end - start}')

get_all_cars()
