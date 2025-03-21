# app/urls.py
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard_landing_page, name='dashboard_landing_page'),
]
