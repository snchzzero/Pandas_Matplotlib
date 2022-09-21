from django.shortcuts import render, redirect
from pnds_mtpltlb.forms import Form_Action, Form_Sort
from datetime import datetime
import psycopg2
from pnds_mtpltlb.data_analyst import db_insert_data, google_API_send, sort_tab, analyst_data
from pnds_mtpltlb.config_db import host, user, password, db_name
from pnds_mtpltlb.data_plot import build_plot
import os

global name
name = 'home'

def time():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # получаем текущее время
    return(now)

def home(request):
    name = 'home'
    if request.method == 'GET':
        return render(request, 'pnds_mtpltlb/home.html', {'form': Form_Action(),
                                                          'now': time(), 'name': name})
    elif request.method == 'POST':
        form = Form_Action(request.POST)
        if form.is_valid():
            analysis_f = form.cleaned_data.get("Analysis_Model")
            show_web_tab_f = form.cleaned_data.get("ShowWebTab_Model")
            send_data_gs_f = form.cleaned_data.get("SendDateGS_Model")
            create_plot_f = form.cleaned_data.get("CreatePlot_Model")
            show_plot_f = form.cleaned_data.get("ShowPlot_Model")

        else:
            analysis_f = ("NO_analysis")
            show_web_tab_f = ("NO_show_web_tab")
            send_data_gs_f = ("NO_send_data_gs")
            create_plot_f = ("NO_create_plot")
            show_plot_f = ("NO_show_plot")

        if analysis_f == "analysis":
            try:
                analyst_data()
                db_insert_data()
                name = "импорт входных данных Google Sheets, анализ данных - завершен"
                return render(request, 'pnds_mtpltlb/home.html',
                            {'form': Form_Action(), 'name': name, 'now': time()})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/home.html',
                              {'form': Form_Action(), 'name': str(name), 'now': time()})
        elif show_web_tab_f == "show_web_tab":
            return redirect('show_web_tab')
        elif send_data_gs_f == "send_data":
            try:
                google_API_send()
                name = 'данные успешно отправлены в Google Sheets'
                return render(request, 'pnds_mtpltlb/home.html',
                              {'form': Form_Action(), 'name': name, 'now': time()})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/home.html',
                              {'form': Form_Action(), 'name': str(name), 'now': time()})
        elif create_plot_f == "create_plot":
            try:
                build_plot()
                name = 'графики рассеяния успешно созданы'
                return render(request, 'pnds_mtpltlb/home.html',
                            {'form': Form_Action(), 'name': name, 'now': time()})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/home.html',
                              {'form': Form_Action(), 'name': str(name), 'now': time()})

        elif show_plot_f == "show_plot":
            return redirect('show_plot')
        else:
            return render(request, 'pnds_mtpltlb/home.html', {'form': Form_Action(), 'now': time(), 'name': name})

def analysis(request):
    pass

def show_web_tab(request):
    global rows

    if request.method == 'GET':
        name = "web таблица успешно загружена"
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name)
            connection.autocommit = True  # что бы не писать после каждого запроса коммит

            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT id, area, cluster, cluster_name, keyword, count, x, y, color FROM pnds_mtpltlb""")
                rows = cursor.fetchall()
                sorts_1_f = 'area'
                sorts_AD_1_f = "возрастанию"
                sorts_2_f = 'cluster'
                sorts_AD_2_f = "возрастанию"
                sorts_3_f = 'cluster name'
                sorts_AD_3_f = "возрастанию"
                sorts_4_f = 'count'
                sorts_AD_4_f = "убыванию"

                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),'name': name, 'now': time(),
                                                                     'rows': rows,
                                                                     'sorts_1_f': sorts_1_f,
                                                                     'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f,
                                                                     'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f,
                                                                     'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f,
                                                                     'sorts_AD_4_f': sorts_AD_4_f})
        except ValueError:
            return render(request, 'pnds_mtpltlb/web_tab.html', {'name': 'Error while working with PostgreSQL'})
        finally:
            if connection:  # закрываем подключение к БД
                connection.close()

    elif request.method == 'POST':
        form = Form_Action(request.POST)
        form2 = Form_Sort(request.POST)
        if form.is_valid():
            analysis_f = form.cleaned_data.get("Analysis_Model")
            show_web_tab_f = form.cleaned_data.get("ShowWebTab_Model")
            send_data_gs_f = form.cleaned_data.get("SendDateGS_Model")
            create_plot_f = form.cleaned_data.get("CreatePlot_Model")
            show_plot_f = form.cleaned_data.get("ShowPlot_Model")
        else:
            analysis_f = ("NO_analysis")
            show_web_tab_f = ("NO_show_web_tab")
            send_data_gs_f = ("NO_send_data_gs")
            create_plot_f = ("NO_create_plot")
            show_plot_f = ("NO_show_plot")

        if form2.is_valid():
            sorts_1_f = form2.cleaned_data.get("sorts_1_Model")
            sorts_AD_1_f = form2.cleaned_data.get("ASC_DESC_1_Model")
            sorts_2_f = form2.cleaned_data.get("sorts_2_Model")
            sorts_AD_2_f = form2.cleaned_data.get("ASC_DESC_2_Model")
            sorts_3_f = form2.cleaned_data.get("sorts_3_Model")
            sorts_AD_3_f = form2.cleaned_data.get("ASC_DESC_3_Model")
            sorts_4_f = form2.cleaned_data.get("sorts_4_Model")
            sorts_AD_4_f = form2.cleaned_data.get("ASC_DESC_4_Model")
            Sort_Default = form2.cleaned_data.get("Sort_Default_Model")

        else:
            sorts_1_f = 'area'
            sorts_AD_1_f = "возрастанию"
            sorts_2_f = 'cluster'
            sorts_AD_2_f = "возрастанию"
            sorts_3_f = 'cluster name'
            sorts_AD_3_f = "возрастанию"
            sorts_4_f = 'count'
            sorts_AD_4_f = "убыванию"
            Sort_Default = "novalue"

        print(sorts_1_f, sorts_AD_1_f, sorts_2_f, sorts_AD_2_f, sorts_3_f, sorts_AD_3_f, sorts_4_f, sorts_AD_4_f, Sort_Default)
        if analysis_f == "analysis":
            try:
                analyst_data()
                db_insert_data()
                name = "импорт входных данных Google Sheets, анализ данных - завершен"
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(), 'name': name,
                                                                     'now': time(), 'rows': rows,
                                                                     'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(), 'name': str(name),
                                                                     'now': time(), 'rows': rows,
                                                                     'sorts_1_f': sorts_1_f,
                                                                     'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f,
                                                                     'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f,
                                                                     'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f,
                                                                     'sorts_AD_4_f': sorts_AD_4_f})
        elif show_web_tab_f == "show_web_tab":
            return redirect('show_web_tab')
        elif send_data_gs_f == "send_data":
            try:
                google_API_send()
                name = 'данные успешно отправлены в Google Sheets'
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': name, 'now': time(), 'rows': rows,
                               'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                               'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                               'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                               'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': str(name), 'now': time(), 'rows': rows,
                               'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                               'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                               'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                               'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
        elif create_plot_f == "create_plot":
            try:
                build_plot()
                name = 'графики рассеяния успешно созданы'
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': name, 'now': time(), 'rows': rows,
                               'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                               'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                               'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                               'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': str(name), 'now': time(), 'rows': rows,
                               'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                               'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                               'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                               'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
        elif show_plot_f == "show_plot":
            return redirect('show_plot')

        # если применена сортировка или осталась сортировка по умолчанию
        elif ((sorts_1_f != 'area' or sorts_AD_1_f != "возрастанию" or sorts_2_f != 'cluster' or\
            sorts_AD_2_f != "возрастанию" or sorts_3_f != 'cluster name' or sorts_AD_3_f != "возрастанию" or\
            sorts_4_f != 'count' or sorts_AD_4_f != "убыванию") and Sort_Default != 'применить') or \
                ((sorts_1_f == 'area' and sorts_AD_1_f == "возрастанию" and sorts_2_f == 'cluster' and \
                sorts_AD_2_f == "возрастанию" and sorts_3_f == 'cluster name' and sorts_AD_3_f == "возрастанию" and \
                sorts_4_f == 'count' and sorts_AD_4_f == "убыванию") and Sort_Default != 'применить'):
            if (sorts_1_f == 'area' and sorts_AD_1_f == "возрастанию" and sorts_2_f == 'cluster' and \
                sorts_AD_2_f == "возрастанию" and sorts_3_f == 'cluster name' and sorts_AD_3_f == "возрастанию" and \
                sorts_4_f == 'count' and sorts_AD_4_f == "убыванию"):
                name = "применена сортировка по умолчанию"
            else:
                name = "применена сортировка пользователя"
            try:
                print('Пытаемся подключиться к базе')
                d1 = {"возрастанию": True, "убыванию": False}
                print(f'{sorts_1_f} {d1[sorts_AD_1_f]} \n{sorts_2_f} {d1[sorts_AD_2_f]} \n{sorts_3_f} {d1[sorts_AD_3_f]} \n{sorts_4_f} {d1[sorts_AD_4_f]}')
                print('Пытаемся применить сортировку')
                sort_tab(column_1=("_").join(sorts_1_f.split()), column_2=("_").join(sorts_2_f.split()),
                         column_3=("_").join(sorts_3_f.split()), column_4=("_").join(sorts_4_f.split()),
                         asc_1=d1[sorts_AD_1_f], asc_2=d1[sorts_AD_2_f], asc_3=d1[sorts_AD_3_f],
                         asc_4=d1[sorts_AD_4_f])
                db_insert_data()

                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name)
                connection.autocommit = True  # что бы не писать после каждого запроса коммит

                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT id, area, cluster, cluster_name, keyword, count, x, y, color FROM pnds_mtpltlb""")
                    rows = cursor.fetchall()

                    return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                         'name': name, 'now': time(), 'rows': rows,
                                                                         'sorts_1_f': sorts_1_f,
                                                                         'sorts_AD_1_f': sorts_AD_1_f,
                                                                         'sorts_2_f': sorts_2_f,
                                                                         'sorts_AD_2_f': sorts_AD_2_f,
                                                                         'sorts_3_f': sorts_3_f,
                                                                         'sorts_AD_3_f': sorts_AD_3_f,
                                                                         'sorts_4_f': sorts_4_f,
                                                                         'sorts_AD_4_f': sorts_AD_4_f
                                                                         })
            except ValueError as name:
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                     'name': str(name), 'now': time(), 'rows': rows,
                                                                     'sorts_1_f': sorts_1_f,
                                                                     'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f,
                                                                     'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f,
                                                                     'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f,
                                                                     'sorts_AD_4_f': sorts_AD_4_f
                                                                     })
            finally:
                if connection:  # закрываем подключение к БД
                    connection.close()

        # кнопка применить сортировку по умолчанию
        elif Sort_Default == 'применить':
            print('новая кнопка сортировка по умолчанию')
            name = "применена сортировка по умолчанию"
            try:
                sort_tab()
                db_insert_data()
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name)
                connection.autocommit = True  # что бы не писать после каждого запроса коммит

                with connection.cursor() as cursor:
                    cursor.execute("""
                                SELECT id, area, cluster, cluster_name, keyword, count, x, y, color FROM pnds_mtpltlb""")
                    rows = cursor.fetchall()

                    sorts_1_f = 'area'
                    sorts_AD_1_f = "возрастанию"
                    sorts_2_f = 'cluster'
                    sorts_AD_2_f = "возрастанию"
                    sorts_3_f = 'cluster name'
                    sorts_AD_3_f = "возрастанию"
                    sorts_4_f = 'count'
                    sorts_AD_4_f = "убыванию"

                    return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                         'name': name, 'now': time(), 'rows': rows,
                                                                         'sorts_1_f': sorts_1_f,
                                                                         'sorts_AD_1_f': sorts_AD_1_f,
                                                                         'sorts_2_f': sorts_2_f,
                                                                         'sorts_AD_2_f': sorts_AD_2_f,
                                                                         'sorts_3_f': sorts_3_f,
                                                                         'sorts_AD_3_f': sorts_AD_3_f,
                                                                         'sorts_4_f': sorts_4_f,
                                                                         'sorts_AD_4_f': sorts_AD_4_f
                                                                         })
            except ValueError as name:
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                     'name': str(name), 'now': time(), 'rows': rows,
                                                                     'sorts_1_f': sorts_1_f,
                                                                     'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f,
                                                                     'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f,
                                                                     'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f,
                                                                     'sorts_AD_4_f': sorts_AD_4_f
                                                                     })
            finally:
                if connection:  # закрываем подключение к БД
                    connection.close()

        else:
            name = "ошибка"
            return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                 'name': name, 'now': time(), 'rows': rows,
                                                                 'sorts_1_f': sorts_1_f,
                                                                 'sorts_AD_1_f': sorts_AD_1_f,
                                                                 'sorts_2_f': sorts_2_f,
                                                                 'sorts_AD_2_f': sorts_AD_2_f,
                                                                 'sorts_3_f': sorts_3_f,
                                                                 'sorts_AD_3_f': sorts_AD_3_f,
                                                                 'sorts_4_f': sorts_4_f,
                                                                 'sorts_AD_4_f': sorts_AD_4_f
                                                                 })

def send_data(request):
    pass

def create_plot(request):
    pass

def show_plot(request):
    form = Form_Action(request.POST)
    if request.method == 'GET':
        if len(os.listdir('pnds_mtpltlb/static/plot')) > 0:
            name = "show plot"
            return render(request, 'pnds_mtpltlb/show_plot.html', {'form': Form_Action(), 'name': name, 'now': time()})
        else:
            name = "у вас нет графиков"
            return render(request, 'pnds_mtpltlb/show_plot.html', {'form': Form_Action(), 'name': name, 'now': time()})
    elif request.method == 'POST':
        if form.is_valid():
            analysis_f = form.cleaned_data.get("Analysis_Model")
            show_web_tab_f = form.cleaned_data.get("ShowWebTab_Model")
            send_data_gs_f = form.cleaned_data.get("SendDateGS_Model")
            create_plot_f = form.cleaned_data.get("CreatePlot_Model")
            show_plot_f = form.cleaned_data.get("ShowPlot_Model")
        else:
            analysis_f = ("NO_analysis")
            show_web_tab_f = ("NO_show_web_tab")
            send_data_gs_f = ("NO_send_data_gs")
            create_plot_f = ("NO_create_plot")
            show_plot_f = ("NO_show_plot")

        if analysis_f == "analysis":
            analyst_data()
            db_insert_data()
            name = "импорт входных данных Google Sheets, анализ данных - завершен"
            return render(request, 'pnds_mtpltlb/show_plot.html',
                          {'form': Form_Action(), 'name': name, 'now': time()})
        elif show_web_tab_f == "show_web_tab":
            return redirect('show_web_tab')
        elif send_data_gs_f == "send_data":
            try:
                google_API_send()
                name = 'данные успешно отправлены в Google Sheets'
                return render(request, 'pnds_mtpltlb/show_plot.html',
                              {'form': Form_Action(), 'name': name, 'now': time()})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/show_plot.html',
                              {'form': Form_Action(), 'name': str(name), 'now': time()})
        elif create_plot_f == "create_plot":
            try:
                build_plot()
                name = 'графики рассеяния успешно созданы'
                return render(request, 'pnds_mtpltlb/show_plot.html',
                              {'form': Form_Action(), 'name': name, 'now': time()})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/show_plot.html',
                              {'form': Form_Action(), 'name': str(name), 'now': time()})


        elif show_plot_f == "show_plot":
            return redirect('show_plot')
        else:
            return render(request, 'pnds_mtpltlb/show_plot.html', {'form': Form_Action(), 'now': time()})