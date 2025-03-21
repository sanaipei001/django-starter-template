from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, MenteeProfile, CaseManagerProfile
from .forms import UserRegisterForm, UserProfileForm, MenteeProfileForm, CaseManagerProfileForm  # Add these imports

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, f'Account created for {user.email}! Welcome to Soiliport.')
            if user.type == User.Types.MENTEE:
                return redirect('mentee:dashboard')
            else:  # User.Types.CASE_MANAGER
                return redirect('case_manager:dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.email}!')
            if user.type == User.Types.MENTEE:
                return redirect('mentee:dashboard')
            else:  # User.Types.CASE_MANAGER
                return redirect('case_manager:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'users/login.html', {})

def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def profile(request):
    user = request.user

    # Initialize forms
    user_form = UserProfileForm(instance=user)
    if user.type == User.Types.MENTEE:
        profile_form = MenteeProfileForm(instance=user.mentee_profile)
    else:  # User.Types.CASE_MANAGER
        profile_form = CaseManagerProfileForm(instance=user.case_manager_profile)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if user.type == User.Types.MENTEE:
            profile_form = MenteeProfileForm(request.POST, instance=user.mentee_profile)
        else:  # User.Types.CASE_MANAGER
            profile_form = CaseManagerProfileForm(request.POST, instance=user.case_manager_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    if user.type == User.Types.MENTEE:
        context = {
            'user': user,
            'profile': user.mentee_profile,
            'case_manager': user.mentee_profile.case_manager if user.mentee_profile else None,
            'user_form': user_form,
            'profile_form': profile_form,
        }
    else:  # User.Types.CASE_MANAGER
        mentees = user.assigned_mentees.all()
        context = {
            'user': user,
            'profile': user.case_manager_profile,
            'mentees': mentees,
            'mentee_count': user.assigned_mentees.count(),
            'user_form': user_form,
            'profile_form': profile_form,
        }
    return render(request, 'users/profile.html', context)

@login_required
def assign_case_manager(request, mentee_id):
    if request.user.type != User.Types.CASE_MANAGER or not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('users:profile')
    
    mentee = get_object_or_404(User, id=mentee_id, type=User.Types.MENTEE)
    case_manager = request.user
    
    if case_manager.case_manager_profile and case_manager.assigned_mentees.count() < case_manager.case_manager_profile.max_mentee_capacity:
        mentee.mentee_profile.case_manager = case_manager
        mentee.mentee_profile.save()
        messages.success(request, f'Assigned {case_manager.email} to {mentee.email}.')
    else:
        messages.error(request, 'Cannot assign more mentees to this case manager.')
    
    return redirect('users:profile')

@login_required
def dashboard_redirect(request):
    if request.user.type == User.Types.MENTEE:
        return redirect('mentee:dashboard')
    else:  # User.Types.CASE_MANAGER
        return redirect('case_manager:dashboard')