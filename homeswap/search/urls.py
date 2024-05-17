from django.urls import path
from .views import search_view, search_form_view

app_name = 'search'

urlpatterns = [
    path('api/search/', search_view, name='search'),
    path('form/', search_form_view, name='search_form'),
]