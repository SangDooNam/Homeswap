# messaging/forms.py

from django import forms
from .models import SupportRequest
from .models import Deposit

class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['email', 'subject', 'message']

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = []
    
    def __init__(self, *args, **kwargs):
        self.field_name = kwargs.pop('field_name', None)
        super(DepositForm, self).__init__(*args, **kwargs)
        if self.field_name:
            self.fields[self.field_name] = self.Meta.model._meta.get_field(self.field_name).formfield()