from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class ValidateModel(models.Model):
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        
        abstract = True


class AppUser(AbstractUser):
    
    profile_photo = models.ImageField(upload_to='profile_photo', default='profile_photo/default.jpg')
    phone_number = PhoneNumberField(null=True, blank=True, region='DE')
    biography = models.TextField(null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    max_capacity = models.SmallIntegerField(null=True, blank=True)
    postal_code = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.username


class HomePhoto(ValidateModel):
    
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='home_photos')
    image = models.ImageField(upload_to='home_photos', null=True, blank=True)
    photo_type = models.CharField(max_length=50, help_text="Type of the Photo, e.g., 'kitchen', 'living room'.")
    
    def __str__(self):
        return f"{self.user.username} - {self.photo_type}"