# app/views.py
from django.shortcuts import render


def landing_page(request):
    return render(request, 'app/landing_page.html', {'title': 'Welcome'})


def dashboard_landing_page(request):
    return render(request, 'app/dashboard_landing_page.html', {'title': 'Dashboard'})
