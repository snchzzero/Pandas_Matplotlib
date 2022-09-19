from django.shortcuts import render, redirect
from pnds_mtpltlb.forms import Form_Action
from datetime import datetime
from pnds_mtpltlb.data_analyst import analyst_data

global name
name = 'home'

def time():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # получаем текущее время
    return(now)

def home(request):
    if request.method == 'GET':
        return render(request, 'pnds_mtpltlb/home.html', {'form': Form_Action(), 'now': time(), 'name': name})
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
            return redirect('analysis')
        elif show_web_tab_f == "show_web_tab":
            return redirect('show_web_tab')
        elif send_data_gs_f == "send_data":
            return redirect('send_data')
        elif create_plot_f == "create_plot":
            return redirect('create_plot')
        elif show_plot_f == "show_plot":
            return redirect('show_plot')
        else:
            return render(request, 'pnds_mtpltlb/home.html', {'form': Form_Action(), 'now': time(), 'name': name})

def analysis(request):
    global name
    name = "импорт входных данных Google Sheets, анализ данных"
    analyst_data()
    return render(request, 'pnds_mtpltlb/home.html', {'form': Form_Action(), 'name': name, 'now': time()})

def show_web_tab(request):
    pass

def send_data(request):
    pass

def create_plot(request):
    pass

def show_plot(request):
    pass