from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib import messages

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


@login_required
def dashboard(request):
    recent_reports = [
        {"title": "Malaria Outbreak in Region A", "date": "2024-10-01"},
        {"title": "Cholera Case in Village B", "date": "2024-09-25"},
        {"title": "Marburg Outhbreak in Rwanda", "date": "2024-09-30"},
        {"title": "MPox outbreak in East Africa", "date": "2024-09-01"},


    ]
    context = {
        "recent_reports": recent_reports,
        "user": request.user,
    }
    return render(request, 'reports/dashboard.html', context)
