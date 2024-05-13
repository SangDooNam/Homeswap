from django.urls import path
from .views import submit_support_request

urlpatterns = [
    path('submit/', submit_support_request, name='submit_support_request'),
    # Add more URLs as needed
]

