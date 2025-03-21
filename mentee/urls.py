# mentee/urls.py
from django.urls import path
from . import views

app_name = 'mentee'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Add the dashboard URL
    path('survey/create/', views.survey_create, name='survey_create'),
    path('survey/list/', views.survey_list, name='survey_list'),
    path('progress/create/', views.progress_create, name='progress_create'),
    path('progress/list/', views.progress_list, name='progress_list'),
    path('reflection/create/', views.reflection_create, name='reflection_create'),
    path('reflection/list/', views.reflection_list, name='reflection_list'),
    path('recommendation/list/', views.recommendation_list, name='recommendation_list'),
]