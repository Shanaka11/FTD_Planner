from django.db import models

class Repeat(models.TextChoices):
    NEVER = 'Never'
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    BIWEEKLY = 'Biweekly'
    MONTHLY = 'Monthly'