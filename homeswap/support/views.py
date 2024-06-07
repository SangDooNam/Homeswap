from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SupportForm, DepositForm
from messaging.models import Room
from .models import Deposit
from blog.models import BlogPost
from accounts.models import AppUser

def submit_support_request(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            # Process the support request
            # For example, save the support request to the database
            form.save()

            # Send a response email to the user
            user_email = form.cleaned_data['email']  # Assuming 'email' is the field for user's email address
            send_support_response_email(user_email)

            # Optionally, you can display a success message or redirect the user to a thank you page
            return render(request, 'support/thank_you.html')
    else:
        form = SupportForm()

    return render(request, 'support/submit_support_request.html', {'form': form})


def send_support_response_email(user_email):
    # Define the email subject and message
    subject = 'Thank you for your support request'
    message = 'We have received your support request and will respond as soon as possible.'

    # Set the sender email address
    sender_email = settings.EMAIL_HOST_USER  # Use the email address specified in settings

    # Send the email
    send_mail(subject, message, sender_email, [user_email])


@login_required
def deposit_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    deposit = get_object_or_404(Deposit, room=room)
    if request.method == 'POST':
        form = DepositForm(request.POST, instance=deposit)
        if form.is_valid():
            deposit = form.save()
            return redirect('support:update_payment_status', deposit_id=deposit.id)
    else:
        form = DepositForm(instance=deposit)
    
    return render(request, 'main/deposit.html', {'form': form, 'room': room})

@login_required
def update_payment_status(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    target_user = None
    
    if request.user == deposit.sender_user:
        deposit.is_paid_by_sender = True
        target_user = deposit.receiver_user
    elif request.user == deposit.receiver_user:
        deposit.is_paid_by_receiver = True
        target_user = deposit.sender_user
    
    deposit.save()
    
    is_paid = 'false'
    
    if deposit.is_paid:
        is_paid = 'true'
        send_system_message_to_chat(deposit.room, "Both users have successfully paid the deposit.")
        return redirect('support:success_payment', is_paid=is_paid, target_user_id=target_user.id)
    
    return redirect('support:success_payment', is_paid=is_paid, target_user_id=target_user.id)


class DepositPaymentSuccessView(LoginRequiredMixin,TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.is_paid = kwargs.get('is_paid', 'false')
        self.target_user_id = kwargs.get('target_user_id', None)
        return super().dispatch(request, *args, **kwargs)
    def get_template_names(self) -> list[str]:
        if self.is_paid == 'true':
            
            return 'main/is_paid.html'
        return 'main/pending.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        
        if self.is_paid == 'true':
            is_paid = True
        else:
            is_paid = False
        
        target_user = get_object_or_404(AppUser, pk=self.target_user_id)
        target_user_blog = get_object_or_404(BlogPost, user=target_user)
        context['target_user_blog'] = target_user_blog
        context['is_paid'] = is_paid
        context['object_user'] = target_user.username
        return context


def send_system_message_to_chat(room, message):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    from django.conf import settings
    from messaging.models import Message
    from accounts.models import AppUser

    channel_layer = get_channel_layer()
    system_user_id = settings.SYSTEM_USER_ID  
    system_user = AppUser.objects.get(id=system_user_id)
    
    room_group_name = f'chat_{room.room_name}'
    
    system_message = Message.objects.create(
        sender_user=system_user,
        receiver_user=room.receiver_user if room.sender_user == system_user else room.sender_user,
        room=room,
        message=message
    )
    system_message.save()
    
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'chat_message',
            'message': message,
            'sender_name': 'System'
        }
    )
