from django.urls import path
from .views import (RegistrationView, LogInView, log_out)

app_name = 'accounts'

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
