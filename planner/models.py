# Django
from timeit import repeat
from django.db import models
from django.contrib.auth.models import User
# Local
from .enums import Repeat

# Activity
class Activity(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    repeat = models.CharField(max_length=20, choices=Repeat.choices, default=Repeat.NEVER)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'activity'

# Reservation
class Reservation(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=False, null=False)
    startTime = models.DateTimeField(blank=False, null=False)
    endTime = models.DateTimeField(blank=False, null=False)

    class Meta:
        db_table = 'reservation'