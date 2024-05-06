from django import forms
from django.forms import BaseFormSet, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import HomePhoto, AppUser
from typing import Any


def authenticate_user_or_email(user_or_email, password):

    user = authenticate(user= user_or_email, password=password)

    if user is None:
        try:
            username_by_email = User.objects.get(email=user_or_email)
            
            user = authenticate(user=username_by_email.username, password=password)
        except User.DoesNotExist:
            pass
        
    return user


class LoginForm(forms.Form):
    
    username_or_email = forms.CharField(label='Username or E-mail')
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        username = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')
        
        user = authenticate_user_or_email(username, password)
        
        if user is None:
            raise ValidationError('Invalid login credentials')
        
        self.user = user
        
        return cleaned_data


class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = AppUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = AppUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'street',
            'location',
            'postal_code',
            'biography',
            'profile_photo',
        ]
        labels = {
            'profile_photo': '',
        }
        widgets = {
            'postal_code': forms.NumberInput(attrs={'class': 'no-spinners'}),
        }
        
        
class HomePhotoForm(forms.ModelForm):
    
    class Meta:
        model = HomePhoto
        fields = ['image', 'photo_type']
