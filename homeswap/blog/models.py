from django.db import models
from django.utils import timezone
from accounts.models import AppUser, HomePhoto




class BlogPost(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    max_capacity = models.PositiveIntegerField()
    to_city = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    num_travelers = models.PositiveIntegerField(default=1)
    description = models.TextField()
    
    

    def save(self, *args, **kwargs):
        self.location = self.user.location
        self.max_capacity = self.user.max_capacity
        super().save(*args, **kwargs)
