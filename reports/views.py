from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import HealthReportForm, UserRegistrationForm, UserProfileForm
from .models import *

def home(request):
    """Render the home page."""
    return render(request, 'reports/home.html')

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    """Custom login view to handle health worker redirection."""
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # Check logged-in user type
                if hasattr(user, 'userprofile') and user.userprofile.is_health_worker:
                    return redirect('health_worker_dashboard')
                else:
                    return redirect('dashboard')
            else:
                # Authentication failed
                error_message = "Invalid username or password. Please try again."
                return render(request, 'reports/login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()

    return render(request, 'reports/login.html', {'form': form})


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
    messages = SystemContact.objects.filter(reporter=request.user).select_related('health_report').order_by('-date_sent')

    
    content = {
        'reports': reports,
        'user_profile': user_profile,
        'messages': messages,
    }
    return render(request, 'reports/dashboard.html', content)


@login_required
def healthworker_dashboard(request):
    if request.user.userprofile.is_health_worker:
        reports = HealthReport.objects.all()
        user_profile = get_object_or_404(UserProfile, user=request.user)
        total_reports = HealthReport.objects.count()
        resolved_cases = HealthReport.objects.filter(resolved=True).count()
        recent_alerts = Alert.objects.all()[:5]
        total_alerts = Alert.objects.count()
        recent_reports = HealthReport.objects.order_by('-date_reported')[:5]

        context = {
            'total_reports': total_reports,
            'resolved_cases': resolved_cases,
            'recent_alerts': recent_alerts,
            'recent_reports': recent_reports,
            'total_alerts': total_alerts,
            'reports': reports,
            'user_profile': user_profile
        }
        return render(request, 'reports/healthworker_dashboard.html', context)
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
        user = request.user
        form = HealthReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            if hasattr(user, 'userprofile') and user.userprofile.is_health_worker:
                    return redirect('health_worker_dashboard')
            else:
                return redirect('dashboard')
    else:
        form = HealthReportForm()

    return render(request, 'reports/submit_report.html', {'form': form})


@login_required
def view_reports(request):
    # Fetch reports, ordered by unresolved first
    reports = HealthReport.objects.all().order_by('-resolved', '-date_reported')
    return render(request, 'reports/view_reports.html', {'reports': reports})

@login_required
def toggle_report_field(request, report_id, field_name):
    report = get_object_or_404(HealthReport, id=report_id)
    
    if field_name == 'resolved':
        report.resolved = not report.resolved
    elif field_name == 'is_verified':
        report.is_verified = not report.is_verified
    else:
        return JsonResponse({'error': 'Invalid field'}, status=400)
    
    report.save()
    return JsonResponse({'success': True, 'new_value': getattr(report, field_name)})


@login_required
def contact_reporter(request, report_id, method):
    report = get_object_or_404(HealthReport, id=report_id)
    reporter = report.user

    if method == 'system':
        if request.method == 'POST':
            message_content = request.POST.get('message')
            SystemContact.objects.create(reporter=reporter, message=message_content)
            messages.success(request, "Message sent inside the system.")
            return redirect('view_reports')
        return render(request, 'reports/contact_reporter.html', {'report': report, 'reporter': reporter})

    elif method == 'phone':
        messages.info(request, f"Contact {reporter.profile.phone}")
        return redirect('view_reports')

    elif method == 'email':
        messages.info(request, f"Contact via email: {reporter.email}")
        return redirect('view_reports')
