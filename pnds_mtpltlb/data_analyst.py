# для google_API
import random

import httplib2
from googleapiclient import discovery  # вместо apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import csv
import pandas as pd
import json



# для db_google_sheets
import psycopg2
from config import host, user, password, db_name
import requests
import xmltodict

# функция чтения гугл таблицы
def google_API():
    # не забываем расшарить сам документ в гугл таблицах, добавить пользователя из файлы creds.json
    #"client_email": "acountsnchzzero@radiant-planet-353422.iam.gserviceaccount.com",

    # подключение API

    CREDENTIALS_FILE = 'creds.json'  # файл с API
    spreadsheet_id = '18Pzfrg0VEoHBcZqB19Nl7SrcSZ4ivOnQgAQOfYCwe30'  # из url схемы таблицы гугл (Pandas_Matplotlib)

    # документы с которыми будем работать
    creadentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])

    # создаем объект аунтификации
    httpAuth = creadentials.authorize(httplib2.Http())

    # создаем обертку API из которой мы будем получать данные из нашей схемы (v4 версия API sheets)
    service = discovery.build('sheets', 'v4', http=httpAuth)

    # Читаем данные 'A1:aA10' - диапозон, если весь то range='Лист1'
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='tz_data',
        majorDimension='ROWS').execute()
    #print(values)
    #print()
    #print(values['values'])
    return (values)
    # with open('data.json', 'w') as f:
    #     json.dump(values, f)



def csv_data():
    with open('csv_data.csv', 'w') as f:
        writer = csv.writer(f)
        data = google_API()
        for row in data['values']:
            writer.writerow(row)
        print("csv_data успешно")

def analyst_data():
    color = ['blue', 'indigo', 'purple', 'red', 'pink', 'orange', 'yellow', 'green', 'teal', 'cyan', 'gray']

    # Сброс ограничений на количество выводимых рядов
    pd.set_option('display.max_rows', None)
    # Сброс ограничений на число столбцов
    pd.set_option('display.max_columns', None)
    # Сброс ограничений на количество символов в записи
    pd.set_option('display.max_colwidth', None)

    data = pd.read_csv('csv_data.csv', encoding="Windows-1251")  # encoding для чтения русских символов
    #print(data.info())
    data.insert(8, 'color', None)  # добавляем столбец color
    # print(data.info())
    # data.head()
    # print("------------")
    # print(data)
    # for row in data.itertuples():
    #     print(row)
    # print()
    # print()

    d1 = dict()  # для предварительной записи color, что бы не повторялись
    data['count'] = pd.to_numeric(arg=data['count'], errors='coerce', downcast='integer')  # преобразования аргумента(string) в числовую форму

    for row in data.itertuples():  # добавляем в колнку color цвет в соответствии с условием
        #print(row)  # вывести кортеж строки
        if row[1] not in d1:  # если area нет в словаре, то добавляем его и его первый класер + цвет
            col = random.choice(color)
            d1[row[1]] = {row[2]: col}
            #print(sort_data['color'].iloc[row[0]])  # вывести значение цвета (столбец и индекс)
            data.loc[row[0], 'color'] = col
            #print(data['color'].iloc[row[0]])  # получить значение из ячейки
            #print(data.iloc[row[0]])  # получить значение из строки
        elif row[1] in d1 and row[2] in d1[row[1]]:  # если есть аrеа и есть кластер, то просто прибавляем цвет предыдущего кластера
            data.loc[row[0], 'color'] = d1[row[1]][row[2]]
            #print(data.iloc[row[0]])  # получить значение из строки
        elif row[1] in d1 and row[2] not in d1[row[1]]:  # если есть area но нет кластера, прибавляем кластер + новый цвет
            col = random.choice(color)
            while col in d1[row[1]].values():
                col = random.choice(color)
            d1[row[1]][row[2]] = col
            data.loc[row[0], 'color'] = col
            #print(data.iloc[row[0]])  # получить значение из строки

    # sort_data = data.sort_values(by=['area', 'cluster', 'cluster_name', 'count'],
    #                              ascending=[True, True, True, False])  # сортировка по столбцам
    for row in sort_data.itertuples():
        print(row)




    #print(data)


csv_data()
analyst_data()

#google_API()