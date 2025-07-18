# from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('executes',views.executes, name="executes"),
    path('run', views.run, name='run'),
]
