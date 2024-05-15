from django.urls import path
from .views import send_message, message_sent_success

app_name = 'messaging'

urlpatterns = [
    path('send/', send_message, name='send_message'),
    path('send/success/', message_sent_success, name='message_sent_success'),
]

