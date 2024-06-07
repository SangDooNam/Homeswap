from typing import Any
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.views import View
from django.http import HttpRequest, JsonResponse

from accounts.models import AppUser
from .models import Room, Message
from .forms import MessageForm
from django.conf import settings
from support.models import Deposit


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            # Redirect to a success page.
            return redirect('message_sent_success')
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {'form': form})

def message_sent_success(request):
    return render(request, 'messaging/message_sent_success.html')

class GetUser(LoginRequiredMixin, View):
    
    def post(self, request):
        sender = request.user.id
        receiver = request.POST['user_id']
        
        sender_user = AppUser.objects.get(id=sender)
        receiver_user = AppUser.objects.get(id=receiver)
        
        request.session['receiver_user'] = receiver
        
        # Get or create the room
        get_room = Room.objects.filter(
            Q(sender_user=sender_user, receiver_user=receiver_user) | 
            Q(sender_user=receiver_user, receiver_user=sender_user)
        )
        
        if get_room.exists():
            room_name = get_room[0].room_name
        else:
            new_room = get_random_string(10)
            while Room.objects.filter(room_name=new_room).exists():
                new_room = get_random_string(10)
                
            create_room = Room.objects.create(
                sender_user=sender_user,
                receiver_user=receiver_user, 
                room_name=new_room
            )
            create_room.save()
            room_name = create_room.room_name
        
        room = get_object_or_404(Room, room_name=room_name)
        
        # Retrieve all messages related to the room
        messages = Message.objects.filter(room=room).order_by('timestamp')
        
        system_user_id = settings.SYSTEM_USER_ID
        
        messages_list = [
            {
                'sender': message.sender_user.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_system': message.sender_user.id == system_user_id
            }
            for message in messages
        ]
        
        return JsonResponse({
            'room_name': room_name, 
            'sender_name': sender_user.username, 
            'receiver_photo_url': receiver_user.profile_photo.url, 
            'receiver_name': receiver_user.username,
            'messages': messages_list,
        })


class DebugView(View):
    def post(self, request):
        message = request.POST.get('message', 'No message')
        print(f"Debug: {message}")
        return JsonResponse({'status': 'success'})


@login_required
def confirm_swap(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    if request.user == room.sender_user:
        room.sender_confirmed = True
    elif request.user == room.receiver_user:
        room.receiver_confirmed = True
    
    room.save()

    if room.is_confirmed:
        # Both users have confirmed
        Deposit.objects.get_or_create(
            sender_user=room.sender_user,
            receiver_user=room.receiver_user,
            room=room,
            defaults={'sender_amount': 0, 'receiver_amount': 0}
        )
        return JsonResponse({'status': 'success', 'is_confirmed': True})
    
    return JsonResponse({'status': 'success', 'is_confirmed': False})

