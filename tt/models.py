from django.db import models
from django.utils import timezone

class Data(models.Model):
    user = models.ForeignKey('auth.User')
    data = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title