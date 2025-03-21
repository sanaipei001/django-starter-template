# case_manager/urls.py
from django.urls import path
from . import views

app_name = 'case_manager'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mentee/<int:mentee_id>/surveys/', views.mentee_surveys, name='mentee_surveys'),
    path('session/create/', views.session_create, name='session_create'),
    path('session/list/', views.session_list, name='session_list'),
    path('report/create/', views.report_create, name='report_create'),
    path('report/list/', views.report_list, name='report_list'),
]