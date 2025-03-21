# mentee/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Survey, Progress, Reflection, Recommendation
from .forms import SurveyForm, ProgressForm, ReflectionForm, RecommendationForm
from users.models import User

@login_required
def dashboard(request):
    if request.user.type != 'MENTEE':
        messages.error(request, 'Only mentees can access this dashboard.')
        return redirect('users:profile')
    surveys = Survey.objects.filter(mentee=request.user)
    progress_entries = Progress.objects.filter(mentee=request.user)
    reflections = Reflection.objects.filter(mentee=request.user)
    recommendations = Recommendation.objects.filter(mentee=request.user)
    return render(request, 'mentee/dashboard.html', {
        'user': request.user,
        'survey_count': surveys.count(),
        'progress_count': progress_entries.count(),
        'reflection_count': reflections.count(),
        'recommendation_count': recommendations.count(),
    })

@login_required
def survey_create(request):
    if request.user.type != 'MENTEE':
        messages.error(request, 'Only mentees can create surveys.')
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.mentee = request.user
            survey.save()
            messages.success(request, 'Survey submitted successfully!')
            return redirect('mentee:survey_list')
    else:
        form = SurveyForm()
    return render(request, 'mentee/survey_form.html', {'form': form})

@login_required
def survey_list(request):
    if request.user.type != 'MENTEE':
        return redirect('users:profile')
    surveys = Survey.objects.filter(mentee=request.user)
    return render(request, 'mentee/survey_list.html', {'surveys': surveys})

@login_required
def progress_create(request):
    if request.user.type != 'MENTEE':
        messages.error(request, 'Only mentees can track progress.')
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.mentee = request.user
            progress.save()
            messages.success(request, 'Progress added successfully!')
            return redirect('mentee:progress_list')
    else:
        form = ProgressForm()
    return render(request, 'mentee/progress_form.html', {'form': form})

@login_required
def progress_list(request):
    if request.user.type != 'MENTEE':
        return redirect('users:profile')
    progress_entries = Progress.objects.filter(mentee=request.user)
    return render(request, 'mentee/progress_list.html', {'progress_entries': progress_entries})

@login_required
def reflection_create(request):
    if request.user.type != 'MENTEE':
        messages.error(request, 'Only mentees can create reflections.')
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = ReflectionForm(request.POST)
        if form.is_valid():
            reflection = form.save(commit=False)
            reflection.mentee = request.user
            reflection.save()
            messages.success(request, 'Reflection submitted successfully!')
            return redirect('mentee:reflection_list')
    else:
        form = ReflectionForm()
    return render(request, 'mentee/reflection_form.html', {'form': form})

@login_required
def reflection_list(request):
    if request.user.type != 'MENTEE':
        return redirect('users:profile')
    reflections = Reflection.objects.filter(mentee=request.user)
    return render(request, 'mentee/reflection_list.html', {'reflections': reflections})

@login_required
def recommendation_list(request):
    if request.user.type != 'MENTEE':
        return redirect('users:profile')
    recommendations = Recommendation.objects.filter(mentee=request.user)
    return render(request, 'mentee/recommendation_list.html', {'recommendations': recommendations})