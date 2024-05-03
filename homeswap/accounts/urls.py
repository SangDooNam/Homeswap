from django.urls import path, include
from .views import (RegistrationView, LogInView, log_out, HomeView, ProfileView,
                    some_view_before_oauth, ProfileEditView, delete_image)
app_name = 'accounts'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logging/', some_view_before_oauth, name='logging'),
    path('profile_edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('delete_image/<int:pk>', delete_image, name='delete_image'),
]
