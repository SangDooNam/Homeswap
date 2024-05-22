from django import forms

class BlogPostSearchForm(forms.Form):
    search_destination = forms.CharField(max_length=100, required=True)
    search_start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    search_end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    search_num_travelers = forms.IntegerField(min_value=1, required=True)