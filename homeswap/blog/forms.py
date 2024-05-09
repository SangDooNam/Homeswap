from django import forms
from .models import BlogPost
from django.utils.dateparse import parse_date
import datetime


class BlogPostForm(forms.ModelForm):
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(
            attrs={
                'type':"date",
            }
        ))
    end_date = forms.DateField(
        label='End Date',
        widget=forms.DateInput(
            attrs={
                'type':"date",
            }
        ))
    
    num_travelers = forms.IntegerField(
        label='Number of travelers'
    )
    

    class Meta:
        model = BlogPost
        fields = ['to_city', 'start_date', 'end_date', 'num_travelers', 'description']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date >= end_date:
            raise forms.ValidationError(
                "End date must be after start date."
            )
        return cleaned_data

