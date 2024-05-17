from django.urls import path, include
from .views import (log_out, HomeView, ProfileView, ProfileEditView, delete_image,
                    DummyView)

app_name = 'accounts'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', log_out, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<str:form_name>', ProfileEditView.as_view(), name='profile_edit'),
    path('delete_image/<int:pk>', delete_image, name='delete_image'),
    path('dummy/', DummyView.as_view(), name='dummy'),
]
