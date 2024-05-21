from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

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
    street = models.CharField(max_length=40, null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    max_capacity = models.SmallIntegerField(null=True, blank=True)
    postal_code = models.CharField(
        max_length=5, 
        null=True, 
        blank=True, 
        validators=[RegexValidator(r'^\d{5}$', 'Postal code should contain exactly 5 digits')]
    )
    birthday_date = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.username

    def clean(self):
        if len(self.street) > 40:
            raise ValidationError({'street': 'street can contain not more 40 letters.'})
        
        if len(self.location) > 40:
            raise ValidationError({'location': 'location can contain not more 40 letters.'})
        
        if self.postal_code and not self.postal_code.isdigit():
            raise ValidationError({'postal_code': 'Postal code should contain exactly 5 digits'})
        
        if len(self.postal_code) > 5:
            raise ValidationError({'postal_code': 'Postal code should contain exactly 5 digits'})
        
        super().clean()

class HomePhoto(ValidateModel):
    
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='home_photos')
    image = models.ImageField(upload_to='home_photos', null=True, blank=True)
    photo_type = models.CharField(max_length=50, help_text="Type of the Photo, e.g., 'kitchen', 'living room'.")
    
    def __str__(self):
        return f"{self.user.username} - {self.photo_type}"