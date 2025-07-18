from django.contrib import admin
from django.urls import path
from . import views

# app_name = 'ojapp'

urlpatterns = [
    path('',views.index, name="index"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout',views.logout_view, name='logout_view'),
    path('problemlist', views.problem_list, name='problem_list'),
    path('problem/<slug:p_name>', views.problems, name="problem"),
    # path()
]
