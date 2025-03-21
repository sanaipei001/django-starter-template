# case_manager/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mentee.models import Survey
from users.models import User
from .models import Session, Report
from .forms import SessionForm, ReportForm

@login_required
def dashboard(request):
    if request.user.type != 'CASE_MANAGER':
        messages.error(request, 'Only case managers can access this dashboard.')
        return redirect('users:profile')
    mentees = request.user.assigned_mentees.all()
    sessions = Session.objects.filter(case_manager=request.user)
    reports = Report.objects.filter(case_manager=request.user)
    return render(request, 'case_manager/dashboard.html', {
        'user': request.user,
        'mentees': mentees,
        'mentee_count': mentees.count(),
        'session_count': sessions.count(),
        'report_count': reports.count(),
    })

@login_required
def mentee_surveys(request, mentee_id):
    if request.user.type != 'CASE_MANAGER':
        return redirect('users:profile')
    mentee = get_object_or_404(User, id=mentee_id, type='MENTEE')
    surveys = Survey.objects.filter(mentee=mentee)
    return render(request, 'case_manager/mentee_surveys.html', {'mentee': mentee, 'surveys': surveys})

@login_required
def session_create(request):
    if request.user.type != 'CASE_MANAGER':
        messages.error(request, 'Only case managers can create sessions.')
        return redirect('users:profile')
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.case_manager = request.user
            session.save()
            messages.success(request, 'Session created successfully!')
            return redirect('case_manager:session_list')
    else:
        form = SessionForm()
        # Limit mentee choices to the case manager's assigned mentees
        form.fields['mentee'].queryset = request.user.assigned_mentees.all()
    return render(request, 'case_manager/session_form.html', {'form': form})

@login_required
def session_list(request):
    if request.user.type != 'CASE_MANAGER':
        return redirect('users:profile')
    sessions = Session.objects.filter(case_manager=request.user)
    return render(request, 'case_manager/session_list.html', {'sessions': sessions})

@login_required
def report_create(request):
    if request.user.type != 'CASE_MANAGER':
        messages.error(request, 'Only case managers can create reports.')
        return redirect('users:profile')
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.case_manager = request.user
            report.save()
            messages.success(request, 'Report created successfully!')
            return redirect('case_manager:report_list')
    else:
        form = ReportForm()
        # Limit mentee choices to the case manager's assigned mentees
        form.fields['mentee'].queryset = request.user.assigned_mentees.all()
    return render(request, 'case_manager/report_form.html', {'form': form})

@login_required
def report_list(request):
    if request.user.type != 'CASE_MANAGER':
        return redirect('users:profile')
    reports = Report.objects.filter(case_manager=request.user)
    return render(request, 'case_manager/report_list.html', {'reports': reports})