from django import forms
from django.contrib.auth.models import User
from .models import *

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    phone_number = forms.CharField(max_length=15)
    is_health_worker = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    """Form for updating the user profile."""
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'is_health_worker']

class HealthReportForm(forms.ModelForm):
    """Form for submitting a health report."""
    class Meta:
        model = HealthReport
        fields = ['incident_type', 'description', 'location']
        widgets = {
            'reported_date': forms.DateInput(attrs={'type': 'date'}),
        }