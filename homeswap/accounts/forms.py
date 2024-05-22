from django import forms
from django.forms import BaseFormSet, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

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
        fields = []
        labels = {
            'profile_photo': '',
        }
        widgets = {
            'postal_code': forms.NumberInput(attrs={'class': 'no-spinners'}),
            'phone_number': PhoneNumberInternationalFallbackWidget(attrs={'region':'DE'}),
        }

    def __init__(self, *args, **kwargs):
        
        self.field_name = kwargs.pop('field_name', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.field_name:
            self.fields[self.field_name] = self.Meta.model._meta.get_field(self.field_name).formfield()
        else:
            self.fields['profile_photo'] = self.Meta.model._meta.get_field('profile_photo').formfield()
            
    def clean(self):
        cleaned_data = super().clean()
        field_value = cleaned_data.get(self.field_name)
        
        if self.field_name == 'max_capacity' and field_value is not None:
            if field_value < 1:
                self.add_error(self.field_name, "Max capacity must be at least 1.")
            elif field_value > 10:
                self.add_error(self.field_name, "Max capacity cannot exceed 10.")
        
        return cleaned_data
            
    def save(self, commit=True):
        instance = super(ProfileForm, self).save(commit=False)
        if self.cleaned_data.get(self.field_name):
            setattr(instance, self.field_name, self.cleaned_data[self.field_name])
        if commit:
            instance.save()
        return instance

class HomePhotoForm(forms.ModelForm):
    
    class Meta:
        model = HomePhoto
        fields = ['image', 'photo_type']
