from django.contrib import admin
from .models import UserProfile, IncidentType, Symptom, HealthReport, Location, Alert

admin.site.register(UserProfile)
admin.site.register(IncidentType)
admin.site.register(Symptom)
admin.site.register(HealthReport)
admin.site.register(Location)
admin.site.register(Alert)