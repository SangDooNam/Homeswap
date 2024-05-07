from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')

    class Meta:
        model = BlogPost
        fields = ['to_city', 'start_date', 'end_date', 'num_travelers', 'description']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "End date must be after start date."
                )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_period = (self.cleaned_data['start_date'], self.cleaned_data['end_date'])
        if commit:
            instance.save()
        return instance