# messaging/forms.py

from django import forms
from .models import SupportRequest

class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['email', 'subject', 'message']
