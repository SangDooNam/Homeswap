from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from accounts.models import AppUser
import datetime as dt

class BlogPost(models.Model):
    title = models.CharField(max_length=100, default='Untitled')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='blog_by_user')
    location = models.CharField(max_length=100)
    max_capacity = models.PositiveIntegerField()
    to_city = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    num_travelers = models.PositiveIntegerField(default=1)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def clean(self) -> None:
        
        if self.start_date < dt.date.today():
            raise ValidationError({'start_date': "Start date can't be older then today"})
        
        if self.end_date and self.end_date < dt.date.today():
            raise ValidationError({'end_date': "End date can't be older then today"})
        
        if self.num_travelers < 1:
            raise ValidationError({'num_travelers': "Number of travelers needs to be at least 1."})
        
        super().clean()