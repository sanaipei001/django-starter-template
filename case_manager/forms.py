# case_manager/forms.py
from django import forms
from .models import Session, Report

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['mentee', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['mentee', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }