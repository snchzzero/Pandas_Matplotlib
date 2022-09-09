# для google_API
import httplib2
from googleapiclient import discovery  # вместо apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


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
    print(values)
    #return (values)

google_API()