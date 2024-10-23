from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class UserProfile(models.Model):
    '''
        Extends the default Django User model with additional fields for health workers
        or other users (regular citizens) who can report incidents.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_health_worker = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

class IncidentType(models.Model):
    '''
        Represents different types of incidents
        e.g., disease outbreak,
        environmental issue[that can lead to an outbreak].
    '''
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    '''
        geographic data for health reports.
        Where are you reporting from.
        Will deal with long n latitude to avoid problems of unknown area names.
        Concerned that the user might find it difficult to enter coordinates? Yes I thought about it,
        The user will use a regular name
        [auto detect location to be implemented too, but not right now].
    '''
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

class Symptom(models.Model):
    '''
        symptoms that can be reported so that we can see a pattern.
    '''
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class HealthReport(models.Model):
    '''
        actual health incidents reported by users.
    '''
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    incident_type = models.ForeignKey(IncidentType, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.incident_type.name} - {self.location.name}"

class Alert(models.Model):
    '''
        alerts generated based on health report patterns or anomalies.
    '''
    report = models.ForeignKey(HealthReport, on_delete=models.CASCADE)
    message = models.TextField()
    date_generated = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert for {self.report.incident_type.name} at {self.report.location.name}"

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()