from django.db import models
from django.conf import settings


class Event(models.Model):
    event_text = models.CharField(max_length=1500)
    important = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_text
