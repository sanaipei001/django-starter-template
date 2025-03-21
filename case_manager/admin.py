# case_manager/admin.py
from django.contrib import admin
from .models import Session, Report

admin.site.register(Session)
admin.site.register(Report)