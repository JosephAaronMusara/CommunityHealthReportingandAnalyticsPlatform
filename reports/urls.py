from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='reports/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('health_worker_dashboard/', views.healthworker_dashboard, name='health_worker_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('submit_report/', views.submit_report, name='submit_report'),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('report/toggle/<int:report_id>/<str:field_name>/', views.toggle_report_field, name='toggle_report_field'),
    path('report/<int:report_id>/contact/<str:method>/', views.contact_reporter, name='contact_reporter'),

]