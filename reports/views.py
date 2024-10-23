from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import UserProfile, HealthReport
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import HealthReportForm, UserRegistrationForm, UserProfileForm

def home(request):
    """Render the home page."""
    return render(request, 'home.html')


def home(request):
    return render(request, 'reports/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            # phone_number = form.cleaned_data['phone_number']
            # is_health_worker = form.cleaned_data['is_health_worker']
            # UserProfile.objects.get_or_create(
            #     user=user,
            #     defaults={'phone_number': phone_number, 'is_health_worker': is_health_worker}
            # )

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

# def login_view(request):
#     """Handle user login."""
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             error_message = "Invalid credentials. Please try again."
#             return render(request, '/templates/reports/login.html', {'error_message': error_message})
#     return render(request, '/templates/reports/login.html')

# def logout_view(request):
#     """Handle user logout."""
#     logout(request)
#     return redirect('home')


# @login_required
# def dashboard(request):
#     recent_reports = [
#         {"title": "Malaria Outbreak in Region A", "date": "2024-10-01"},
#         {"title": "Cholera Case in Village B", "date": "2024-09-25"},
#         {"title": "Marburg Outhbreak in Rwanda", "date": "2024-09-30"},
#         {"title": "MPox outbreak in East Africa", "date": "2024-09-01"},


#     ]
#     context = {
#         "recent_reports": recent_reports,
#         "user": request.user,
#     }
#     return render(request, 'reports/dashboard.html', context)

@login_required
def dashboard(request):
    """User dashboard for submitting and viewing health reports."""
    reports = HealthReport.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'reports': reports})

@login_required
def health_worker_dashboard(request):
    """Dashboard for health workers to manage health reports."""
    if request.user.userprofile.is_health_worker:
        reports = HealthReport.objects.all()  # Show all reports to health workers
        return render(request, 'health_worker_dashboard.html', {'reports': reports})
    else:
        return redirect('dashboard')
    
# views.py

@login_required
def profile_view(request):
    """View and edit user profile."""
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'profile.html', {'profile_form': profile_form})

# views.py

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

    return render(request, 'submit_report.html', {'form': form})

