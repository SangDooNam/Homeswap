from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_city = models.CharField(max_length=100)
    max_capacity = models.PositiveIntegerField()
    to_city = models.CharField(max_length=100)
    date_period = models.DateField()
    num_travelers = models.PositiveIntegerField()
    description = models.TextField()
    

    def save(self, *args, **kwargs):
        user_profile = self.user.userprofile
        self.from_city = user_profile.city
        self.max_capacity = user_profile.max_capacity
        super().save(*args, **kwargs)
