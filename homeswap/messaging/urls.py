from django.urls import path
from .views import send_message, message_sent_success,  GetUser, DebugView, confirm_swap

app_name = 'messaging'

urlpatterns = [
    path('send/', send_message, name='send_message'),
    path('send/success/', message_sent_success, name='message_sent_success'),
    path('chat/', GetUser.as_view(), name='get_user'),
    path('debug/', DebugView.as_view(), name='debug'), 
    path('confirm_swap/<str:room_name>/', confirm_swap, name='confirm_swap'),
]

