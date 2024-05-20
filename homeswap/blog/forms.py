from django import forms
from .models import BlogPost
from django.utils.dateparse import parse_date
import datetime


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'to_city', 'start_date', 'end_date', 'num_travelers', 'description', 'max_capacity']
        
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
    
    max_capacity = forms.IntegerField(disabled=True)
    location = forms.CharField(disabled=True)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BlogPostForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['location'].initial = user.location
            self.fields['max_capacity'].initial = user.max_capacity

    def clean(self):
        cleaned_data = super().clean()
        # print('CLEANED DATA: ',cleaned_data)
        # print('USER: ', self.fields)
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        location = cleaned_data.get("location")
        max_capacity = cleaned_data.get("max_capacity")

        if start_date and end_date and start_date >= end_date:
            self.add_error('end_date', "End date must be after start date.")

        if not location:
            self.add_error('location', "You need to fill in your location on your profile to post.")

        if not max_capacity:
            self.add_error('max_capacity', "You need to fill in the max capacity of your home on your profile to post.")
        
        return cleaned_data

