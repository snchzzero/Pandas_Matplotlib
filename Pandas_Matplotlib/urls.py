"""Pandas_Matplotlib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pnds_mtpltlb import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='gohome'),
    path('analysis/', views.analysis, name='analysis'),
    path('show_web_tab/', views.show_web_tab, name='show_web_tab'),
    path('send_data/', views.send_data, name='send_data'),
    path('create_plot/', views.create_plot, name='create_plot'),
    path('show_plot/', views.show_plot, name='show_plot'),
]
