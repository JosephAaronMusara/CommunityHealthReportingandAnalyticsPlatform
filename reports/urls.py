from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='reports/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('health_worker_dashboard/', views.health_worker_dashboard, name='health_worker_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('submit_report/', views.submit_report, name='submit_report'),
]