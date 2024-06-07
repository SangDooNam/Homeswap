from django.urls import path
from .views import submit_support_request, deposit_view, update_payment_status, DepositPaymentSuccessView

app_name = 'support'

urlpatterns = [
    path('submit/', submit_support_request, name='submit_support_request'),
    # Add more URLs as needed
    path('deposit/<int:room_id>/', deposit_view, name='deposit_view'),
    path('update_payment_status/<int:deposit_id>/', update_payment_status, name='update_payment_status'),
    path('payment_success/<str:is_paid>/<int:target_user_id>/', DepositPaymentSuccessView.as_view(), name='success_payment')
]

