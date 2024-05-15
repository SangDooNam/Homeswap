from django.urls import path
from .views import search_view

app_name = 'search'

urlpatterns = [
    path('api/search/', search_view, name='search'),
]