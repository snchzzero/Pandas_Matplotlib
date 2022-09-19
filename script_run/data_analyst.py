# для google_API
import random

import httplib2
from googleapiclient import discovery  # вместо apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import csv
import pandas as pd
import time
from datetime import datetime

def now():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

# чтение исходных данных Google Sheets
def google_API_get():
    # не забываем расшарить сам документ в гугл таблицах, добавить пользователя из файлы creds.json
    #"client_email": "acountsnchzzero@radiant-planet-353422.iam.gserviceaccount.com",

    # подключение API

    CREDENTIALS_FILE = 'creds.json'  # файл с API
    spreadsheet_id = '18Pzfrg0VEoHBcZqB19Nl7SrcSZ4ivOnQgAQOfYCwe30'  # из url схемы таблицы гугл (Pandas_Matplotlib)

    # документы с которыми будем работать (читаем ключи из файла)
    creadentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])

    # создаем объект аунтификации (авторизуемся в системе)
    httpAuth = creadentials.authorize(httplib2.Http())

    # создаем обертку API из которой мы будем получать данные из нашей схемы (v4 версия API sheets)
    service = discovery.build('sheets', 'v4', http=httpAuth)

    # Читаем данные 'A1:aA10' - диапозон, если весь то range='Лист1'
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='tz_data',
        majorDimension='ROWS').execute()

    print(f'[{now()}] Чтение исходных данных Google Sheets - успешно завершено')
    return (values)

# создание csv файла с прочтенных исходных данных из Google Sheets
def csv_data():
    with open('csv_data.csv', 'w') as f:
        writer = csv.writer(f)
        data = google_API_get()
        for row in data['values']:
            writer.writerow(row)

        print(f'[{now()}] Cоздан файл исходных данных Google Sheets: "csv_data.csv" ')

# формирование DataFrame из csv файла, анализ, обработка, добавление color
def analyst_data():
    csv_data()
    color = ['blue', 'indigo', 'purple', 'red', 'pink', 'orange', 'yellow', 'green', 'teal', 'cyan', 'gray']

    # Сброс ограничений на количество выводимых рядов
    pd.set_option('display.max_rows', None)
    # Сброс ограничений на число столбцов
    pd.set_option('display.max_columns', None)
    # Сброс ограничений на количество символов в записи
    pd.set_option('display.max_colwidth', None)

    data = pd.read_csv('csv_data.csv', encoding="Windows-1251")  # encoding для чтения русских символов
    data.insert(8, 'color', None)  # добавляем столбец color
    d1 = dict()  # для предварительной записи color, keyword, что бы избежать повторов
    data['count'] = pd.to_numeric(arg=data['count'], errors='coerce', downcast='integer')  # преобразования аргумента(string) в числовую форму

    # добавляем в колонку color цвет в соответствии с условием
    # удаляем повтор keyword в одной области area
    for row in data.itertuples():
        #print(row)  # вывести кортеж строки
        if row[1] not in d1:  # если area нет в словаре, то добавляем его и его первый кластер + цвет
            col = random.choice(color)
            d1[row[1]] = {row[2]: col, 'keyword':[row[4]]}
            #print(sort_data['color'].iloc[row[0]])  # вывести значение цвета (столбец и индекс)
            data.loc[row[0], 'color'] = col

            #print(data['color'].iloc[row[0]])  # получить значение из ячейки
            #print(data.iloc[row[0]])  # получить значение из строки

        elif row[1] in d1 and row[4] in d1[row[1]]['keyword']:
            data = data.drop(index=row[0])
        elif row[1] in d1 and row[2] in d1[row[1]]:  # если есть аrеа и есть кластер, то просто прибавляем цвет предыдущего кластера
            data.loc[row[0], 'color'] = d1[row[1]][row[2]]
            d1[row[1]]['keyword'].append(row[4])
            #print(data.iloc[row[0]])  # получить значение из строки
        elif row[1] in d1 and row[2] not in d1[row[1]]:  # если есть area но нет кластера, прибавляем кластер + новый цвет
            col = random.choice(color)
            while col in d1[row[1]].values():
                col = random.choice(color)
            d1[row[1]][row[2]] = col
            d1[row[1]]['keyword'].append(row[4])
            data.loc[row[0], 'color'] = col
            #print(data.iloc[row[0]])  # получить значение из строки

    sort_data = data.sort_values(by=['area', 'cluster', 'cluster_name', 'count'],
                                 ascending=[True, True, True, False])  # сортировка по столбцам
    # sort_data = data.sort_values(by=['keyword', 'count'],
    #                              ascending=[True, False])  # сортировка по столбцам (проверка на дублирующие слова)
    # for row in sort_data.itertuples():
    #     print(row)

    print(f'[{now()}] Анализ данных, сортировка данных, добавление "color" - успешно завершено')
    return sort_data

# отправляем отсортированные данные DataFrame в новый Google Sheets
def google_API_send():

    print(f'[{now()}] Перенос данных в новый Google Sheets')

    # не забываем расшарить сам документ в гугл таблицах, добавить пользователя из файлы creds.json
    #"client_email": "acountsnchzzero@radiant-planet-353422.iam.gserviceaccount.com",

    # подключение API

    CREDENTIALS_FILE = 'creds.json'  # файл с API
    spreadsheet_id = '19WU-rV31bktdBMZR1RM-ODJuuHamwcKaplPAJ-LEItY'  # из url схемы таблицы гугл (Pandas_Matplotlib)

    # документы с которыми будем работать (читаем ключи из файла)
    creadentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])

    # создаем объект аунтификации (авторизуемся в системе)
    httpAuth = creadentials.authorize(httplib2.Http())

    # создаем обертку API из которой мы будем получать данные из нашей схемы (v4 версия API sheets)
    service = discovery.build('sheets', 'v4', http=httpAuth)

    # удаляем ранее занесенные данные в Google Sheets
    def del_tab():
        # сначала полностью очищаем лист
        rangeAll = '{0}!A1:Z'.format("Лист1")
        body = {}
        resultClear = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=rangeAll,
                                                            body=body).execute()

        print(f'[{now()}] Ранее занесенные данные в Google Sheets удалены')

    # меняем ширину столбцов
    def tab_column_siz(startI, endI, size):
        results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": [
            {"updateDimensionProperties":
                {
                "range":
                    {"sheetId": 0,
                     "dimension": "COLUMNS",  # Задаем ширину колонки
                     "startIndex": startI,  # Нумерация начинается с нуля
                     "endIndex": endI  # Со столбца номер startIndex по endIndex - 1 (endIndex не входит!)
                     },
                "properties": {"pixelSize": size  # Ширина в пикселях
                                },
                "fields": "pixelSize"  # Указываем, что нужно использовать параметр pixelSize
                }
            }]}).execute()

        print(f'[{now()}] Меняем ширину столбцов')

    # применяем форматирование текста
    def tab_text_format_main(startRowIndex=0, endRowIndex=0, startColumnIndex=0, endColumnIndex=0, bold=False, fontSize=10 ):
        # Установка формата ячеек
        results = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=
            {"requests": [{"repeatCell": {"cell": {"userEnteredFormat": {"horizontalAlignment": 'CENTER',
                                                                         "textFormat": {"bold": bold,
                                                                                        "fontSize": fontSize}}},
                                          "range": {"sheetId": 0,
                                                    "startRowIndex": startRowIndex,
                                                    "endRowIndex": endRowIndex,
                                                    "startColumnIndex": startColumnIndex,
                                                    "endColumnIndex": endColumnIndex},
                                          "fields": "userEnteredFormat"}}]
            }).execute()

        print(f'[{now()}] Применяем форматирование текста')

    # переноса данных в Google Sheets
    def tab_send_data():
        data = analyst_data()

        print(f'[{now()}] Начат процесс переноса данных в новый Google Sheets')

        # заносим данные в таблицу
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body={
            "valueInputOption": "USER_ENTERED",
            # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": "A1:H1",
                 "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                 "values": [['area', 'cluster', 'cluster_name', 'keyword', 'count', 'x', 'y', 'color'],  # Заполняем первую строку
                 ]}
            ]
        }).execute()

        total = 2
        for row in data.itertuples():
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body={
                "valueInputOption": "USER_ENTERED",
                # Данные воспринимаются, как вводимые пользователем (считается значение формул)
                "data": [
                    {"range": f"A{total}:H{total}",
                     "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                     "values": [
                         [f'{row[1]}', f'{row[2]}', f'{row[3]}', f'{row[4]}', f'{row[6]}', f'{row[7]}', f'{row[8]}', f'{row[9]}'],  # Заполняем первую строку

                     ]}
                ]
            }).execute()
            total += 1
            if total % 50 == 0:  # API quota limitations из-за ограничения делаем паузу на 60сек после каждых 50 запросов

                print(f'[{now()}] Перенесено: {total} - строк. Делаем паузу 60сек. (не перегружаем API)')
                time.sleep(60)
                continue
        return data, total

    del_tab()
    tab_column_siz(0, 2, 80)
    tab_column_siz(3, 4, 300)
    tab_column_siz(4, 5, 80)
    tab_column_siz(5, 7, 150)
    tab_column_siz(7, 8, 80)
    tab_text_format_main(0, 1, 0, 8, True, 10)
    data, endRowIndex = tab_send_data()
    tab_text_format_main(1, endRowIndex, 0, 8, False, 9)

    print(f'[{now()}] Всего перенесено: {endRowIndex} - строк')
    print(f'[{now()}] Перенос данных в Google Sheets(ссылка ниже) - успешно завершено')
    print(f'[{now()}] https://docs.google.com/spreadsheets/d/19WU-rV31bktdBMZR1RM-ODJuuHamwcKaplPAJ-LEItY/edit#gid=0')

    return data

#csv_data()
#analyst_data()
#google_API_send()

