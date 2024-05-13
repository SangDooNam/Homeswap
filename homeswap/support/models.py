# support/models.py
from django.conf import settings
from django.db import models

class SupportRequest(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Support Request from {self.email}'

