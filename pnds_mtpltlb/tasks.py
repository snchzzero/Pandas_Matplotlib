from Pandas_Matplotlib.celery import app

from .data_analyst import google_API_send, analyst_data, db_insert_data, sort_tab, selecet


@app.task
def celery_google_API_send():
    google_API_send()

@app.task
def celery_analyst_data_db_insert_data():
    analyst_data()
    db_insert_data()

@app.task
def celery_sort_tab_db_insert_data(column_1='area', column_2='cluster', column_3='cluster_name', column_4='count',
             asc_1=True, asc_2=True, asc_3=True, asc_4=False):
    sort_tab(column_1=column_1, column_2=column_2, column_3=column_3, column_4=column_4,
             asc_1=asc_1, asc_2=asc_2, asc_3=asc_3, asc_4=asc_4)
    db_insert_data()

@app.task
def celery_selecet():
    rows, name = selecet()
    return rows, name

@app.task
def celery_sort_tab_db_insert_data_selecet(
        column_1='area', column_2='cluster', column_3='cluster_name', column_4='count',
        asc_1=True, asc_2=True, asc_3=True, asc_4=False):
    sort_tab(column_1=column_1, column_2=column_2, column_3=column_3, column_4=column_4,
             asc_1=asc_1, asc_2=asc_2, asc_3=asc_3, asc_4=asc_4)
    db_insert_data()
    rows, name = selecet()
    return rows, name


# #считываем данные по процессору заносим в БД
# @app.task   # оборачиваем в декоратор для отслеживания Celery
# def start_script_insert_date():
#     start_script()
#
# #для формирования csv и построения графиков
# @app.task
# def start_csv_create_figure():
#     csv_all()
#     figure_1()
#     csv_srez()
#     figure_2()
#
# #обнуляем БД
# @app.task
# def for_new_connection():
#     new_connection()