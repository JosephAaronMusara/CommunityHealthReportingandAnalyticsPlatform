from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import HealthReportForm, UserRegistrationForm, UserProfileForm
from .models import UserProfile, HealthReport

def home(request):
    """Render the home page."""
    return render(request, 'reports/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            # Check if UserProfile already exists
            if not UserProfile.objects.filter(user=user).exists():
                phone_number = form.cleaned_data['phone_number']
                is_health_worker = form.cleaned_data['is_health_worker']
                UserProfile.objects.create(
                    user=user,
                    phone_number=phone_number,
                    is_health_worker=is_health_worker
                )

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'reports/register.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard for submitting and viewing health reports."""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    reports = HealthReport.objects.filter(user=request.user)
    
    content = {
        'reports': reports,
        'user_profile': user_profile,
    }
    return render(request, 'reports/dashboard.html', content)


@login_required
def health_worker_dashboard(request):
    """Dashboard for health workers to manage health reports."""
    if request.user.userprofile.is_health_worker:
        reports = HealthReport.objects.all()
        user_profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'reports/health_worker_dashboard.html', {'reports': reports,'user_profile':user_profile})
    else:
        return redirect('login')
 

@login_required
def profile_view(request):
    """View and edit user profile, and change password."""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        password_form = PasswordChangeForm(user=request.user)
        
        if 'update_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
        
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('profile')

    else:
        profile_form = UserProfileForm(instance=user_profile)
        password_form = PasswordChangeForm(user=request.user)
    
    return render(request, 'reports/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'user_profile':user_profile
    })


@login_required
def submit_report(request):
    """Submit a new health report."""
    if request.method == 'POST':
        form = HealthReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect('dashboard')
    else:
        form = HealthReportForm()

    return render(request, 'reports/submit_report.html', {'form': form})

