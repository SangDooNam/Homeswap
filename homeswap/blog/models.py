from django.db import models
from django.utils import timezone
from accounts.models import AppUser




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

