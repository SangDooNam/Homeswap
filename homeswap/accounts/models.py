from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class ValidateModel(models.Model):
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        
        abstract = True


class User(AbstractUser):
    
    profile_photo = models.ImageField(upload_to='profile_photo', default='profile_photo/default.jpg')
    phone_number = PhoneNumberField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    addresse = models.TextField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField(max_length=10, null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.username


class HomePhoto(ValidateModel):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='home_photos')
    image = models.ImageField(upload_to='home_photos', null=True, blank=True)
    photo_type = models.CharField(max_length=50, help_text="Type of the Photo, e.g., 'kitchen', 'living room'.")
    
    def __str__(self):
        return f"{self.user.username} - {self.photo_type}"