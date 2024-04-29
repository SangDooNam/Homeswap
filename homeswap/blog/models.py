from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_city = models.CharField(max_length=100)
    date_period = models.DateRangeField()
    num_travelers = models.PositiveIntegerField()
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.from_city:
            self.from_city = self.user.userprofile.city
        super().save(*args, **kwargs)
