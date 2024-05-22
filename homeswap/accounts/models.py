from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from .validators import validate_postal_code


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
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.username

    def clean(self):
        if self.street and len(self.street) > 40:
            raise ValidationError({'street': 'street can contain not more 40 letters.'})
        
        if self.location and len(self.location) > 40:
            raise ValidationError({'location': 'location can contain not more 40 letters.'})
        
        if self.postal_code:
            if len(self.postal_code) > 10:
                raise ValidationError({'postal_code': 'A postal code can contain a maximum of 10 characters.'})
            validate_postal_code(self.postal_code, 'Any country')
        
        # just for test
        # if self.phone_number and not self.phone_number.is_valid():
        #     raise ValidationError({'phone_number': 'Invalid phone number format.'})
        
        validate_postal_code(self.postal_code, 'Any country')
        
        super().clean()

class HomePhoto(ValidateModel):
    
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='home_photos')
    image = models.ImageField(upload_to='home_photos', null=True, blank=True)
    photo_type = models.CharField(max_length=50, help_text="Type of the Photo, e.g., 'kitchen', 'living room'.")
    
    def __str__(self):
        return f"{self.user.username} - {self.photo_type}"