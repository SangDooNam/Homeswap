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
    birthday_date = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.username


class HomePhoto(ValidateModel):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='home_photos')
    first_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    second_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    third_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    fifth_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    sixth_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    seventh_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    eighth_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    nineth_img = models.ImageField(upload_to='home_photos', null=True, blank=True)
    
    def __str__(self):
        return self.user.username