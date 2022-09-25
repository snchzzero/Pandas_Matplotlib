from django.shortcuts import render, redirect
from pnds_mtpltlb.forms import Form_Action, Form_Sort
from datetime import datetime
import os
from .tasks import celery_google_API_send, celery_analyst_data_db_insert_data, \
    celery_selecet, celery_sort_tab_db_insert_data_selecet, celery_build_plot, celery_get_data

default_values = ['area', 'возрастанию', 'cluster', 'возрастанию',
                  'cluster name', 'возрастанию', 'count', 'убыванию', 'novalue']

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
                celery_analyst_data_db_insert_data.delay()
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
                celery_get_data.delay().get()  # проверяет есть ли импортированные данные с GoogleSheets
                celery_google_API_send.delay()
                name = 'данные успешно отправлены в Google Sheets'
                return render(request, 'pnds_mtpltlb/home.html',
                              {'form': Form_Action(), 'name': name, 'now': time()})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/home.html',
                              {'form': Form_Action(), 'name': str(name), 'now': time()})

        elif create_plot_f == "create_plot":
            try:
                celery_get_data.delay().get()  # проверяет есть ли импортированные данные с GoogleSheets
                celery_build_plot.delay()
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


def show_web_tab(request):
    global rows

    if request.method == 'GET':
        sorts_1_f, sorts_AD_1_f, sorts_2_f, sorts_AD_2_f, sorts_3_f, \
        sorts_AD_3_f, sorts_4_f, sorts_AD_4_f, Sort_Default = default_values

        # если возвращается после выполнения задачи celery 2 параметра (return), то они представлены в виде списка
        # что бы получить данные из return нужно у задачи celery применить метод get()
        try:
            rows, name = celery_selecet.delay().get()
            if rows != None:
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(), 'name': name, 'now': time(),
                                                                     'rows': rows,
                                                                     'sorts_1_f': sorts_1_f,
                                                                     'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f,
                                                                     'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f,
                                                                     'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f,
                                                                     'sorts_AD_4_f': sorts_AD_4_f})
        except Exception as ex:
            ex = str(ex)
            if ex.startswith('relation "pnds_mtpltlb"'):
                name = "name 'DT' is not defined"
            else:
                name = ex
            return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(), 'name': name, 'now': time(),
                                                                 'sorts_1_f': sorts_1_f,
                                                                 'sorts_AD_1_f': sorts_AD_1_f,
                                                                 'sorts_2_f': sorts_2_f,
                                                                 'sorts_AD_2_f': sorts_AD_2_f,
                                                                 'sorts_3_f': sorts_3_f,
                                                                 'sorts_AD_3_f': sorts_AD_3_f,
                                                                 'sorts_4_f': sorts_4_f,
                                                                 'sorts_AD_4_f': sorts_AD_4_f})

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
            sorts_1_f, sorts_AD_1_f, sorts_2_f, sorts_AD_2_f, sorts_3_f,\
            sorts_AD_3_f, sorts_4_f, sorts_AD_4_f, Sort_Default = default_values

        print(sorts_1_f, sorts_AD_1_f, sorts_2_f, sorts_AD_2_f, sorts_3_f, sorts_AD_3_f, sorts_4_f, sorts_AD_4_f, Sort_Default)

        if analysis_f == "analysis":
            try:
                celery_analyst_data_db_insert_data.delay()
                name = "импорт входных данных Google Sheets, анализ данных - завершен"
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(), 'name': name,
                                                                     'now': time(),
                                                                     'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(), 'name': str(name),
                                                                     'now': time(),
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
                celery_google_API_send.delay()
                name = 'данные успешно отправлены в Google Sheets'
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': name, 'now': time(), 'rows': rows,
                               'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                               'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                               'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                               'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': str(name), 'now': time(),
                               'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                               'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                               'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                               'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})

        elif create_plot_f == "create_plot":
            name=''
            try:
                celery_build_plot.delay()
                name = 'графики рассеяния успешно созданы'
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': name, 'now': time(), 'rows': rows,
                               'sorts_1_f': sorts_1_f, 'sorts_AD_1_f': sorts_AD_1_f,
                               'sorts_2_f': sorts_2_f, 'sorts_AD_2_f': sorts_AD_2_f,
                               'sorts_3_f': sorts_3_f, 'sorts_AD_3_f': sorts_AD_3_f,
                               'sorts_4_f': sorts_4_f, 'sorts_AD_4_f': sorts_AD_4_f})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/web_tab.html',
                              {'form': Form_Action(), 'form2': Form_Sort(), 'name': str(name), 'now': time(),
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
                rows, name2 = celery_sort_tab_db_insert_data_selecet.delay(
                    column_1=("_").join(sorts_1_f.split()), column_2=("_").join(sorts_2_f.split()),
                    column_3=("_").join(sorts_3_f.split()), column_4=("_").join(sorts_4_f.split()),
                    asc_1=d1[sorts_AD_1_f], asc_2=d1[sorts_AD_2_f], asc_3=d1[sorts_AD_3_f],
                    asc_4=d1[sorts_AD_4_f]).get()

                if rows != None:
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
                else:
                    return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                         'name': name2, 'now': time(),
                                                                         'sorts_1_f': sorts_1_f,
                                                                         'sorts_AD_1_f': sorts_AD_1_f,
                                                                         'sorts_2_f': sorts_2_f,
                                                                         'sorts_AD_2_f': sorts_AD_2_f,
                                                                         'sorts_3_f': sorts_3_f,
                                                                         'sorts_AD_3_f': sorts_AD_3_f,
                                                                         'sorts_4_f': sorts_4_f,
                                                                         'sorts_AD_4_f': sorts_AD_4_f
                                                                         })
            except Exception as ex:
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                     'name': str(ex), 'now': time(),
                                                                     'sorts_1_f': sorts_1_f,
                                                                     'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f,
                                                                     'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f,
                                                                     'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f,
                                                                     'sorts_AD_4_f': sorts_AD_4_f
                                                                     })

        # кнопка применить сортировку по умолчанию
        elif Sort_Default == 'применить':
            try:
                print('новая кнопка сортировка по умолчанию')
                name = "применена сортировка по умолчанию"
                rows, name2 = celery_sort_tab_db_insert_data_selecet.delay().get()

                sorts_1_f, sorts_AD_1_f, sorts_2_f, sorts_AD_2_f, sorts_3_f, \
                sorts_AD_3_f, sorts_4_f, sorts_AD_4_f, Sort_Default = default_values

                if rows != None:
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
                else:
                    return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                         'name': name2, 'now': time(),
                                                                         'sorts_1_f': sorts_1_f,
                                                                         'sorts_AD_1_f': sorts_AD_1_f,
                                                                         'sorts_2_f': sorts_2_f,
                                                                         'sorts_AD_2_f': sorts_AD_2_f,
                                                                         'sorts_3_f': sorts_3_f,
                                                                         'sorts_AD_3_f': sorts_AD_3_f,
                                                                         'sorts_4_f': sorts_4_f,
                                                                         'sorts_AD_4_f': sorts_AD_4_f
                                                                         })
            except Exception as ex:
                sorts_1_f, sorts_AD_1_f, sorts_2_f, sorts_AD_2_f, sorts_3_f, \
                sorts_AD_3_f, sorts_4_f, sorts_AD_4_f, Sort_Default = default_values
                return render(request, 'pnds_mtpltlb/web_tab.html', {'form': Form_Action(),
                                                                     'name': str(ex), 'now': time(),
                                                                     'sorts_1_f': sorts_1_f,
                                                                     'sorts_AD_1_f': sorts_AD_1_f,
                                                                     'sorts_2_f': sorts_2_f,
                                                                     'sorts_AD_2_f': sorts_AD_2_f,
                                                                     'sorts_3_f': sorts_3_f,
                                                                     'sorts_AD_3_f': sorts_AD_3_f,
                                                                     'sorts_4_f': sorts_4_f,
                                                                     'sorts_AD_4_f': sorts_AD_4_f
                                                                     })

def show_plot(request):
    form = Form_Action(request.POST)
    if request.method == 'GET':
        if len(os.listdir('pnds_mtpltlb/static/plot')) > 1:
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
            celery_analyst_data_db_insert_data.delay()
            name = "импорт входных данных Google Sheets, анализ данных - завершен"
            return render(request, 'pnds_mtpltlb/show_plot.html',
                          {'form': Form_Action(), 'name': name, 'now': time()})
        elif show_web_tab_f == "show_web_tab":
            return redirect('show_web_tab')

        elif send_data_gs_f == "send_data":
            try:
                if celery_get_data.delay().get() == True:  # проверяет есть ли импортированные данные с GoogleSheets
                    celery_google_API_send.delay()
                    name = 'данные успешно отправлены в Google Sheets'
                    return render(request, 'pnds_mtpltlb/show_plot.html',
                                  {'form': Form_Action(), 'name': name, 'now': time()})
            except Exception as name:
                return render(request, 'pnds_mtpltlb/show_plot.html',
                              {'form': Form_Action(), 'name': str(name), 'now': time()})

        elif create_plot_f == "create_plot":
            try:
                if celery_get_data.delay().get() == True:  # проверяет есть ли импортированные данные с GoogleSheets
                    celery_build_plot.delay()
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