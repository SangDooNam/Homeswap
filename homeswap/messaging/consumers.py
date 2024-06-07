import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.apps import apps
from django.conf import settings


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_name = text_data_json['sender_name']
        sender_id = text_data_json.get('sender')
        receiver_id = text_data_json['receiver']
        room_name = text_data_json['room']

        # Lazy load models
        Message = apps.get_model('messaging', 'Message')
        AppUser = apps.get_model('accounts', 'AppUser')
        Room = apps.get_model('messaging', 'Room')

        # Use the system user if sender_id is None
        if sender_id is None:
            sender_user = AppUser.objects.get(id=settings.SYSTEM_USER_ID)
        else:
            sender_user = AppUser.objects.get(id=sender_id)

        receiver_user = AppUser.objects.get(id=receiver_id)
        current_room = Room.objects.get(room_name=room_name)

        # Save message to the database
        new_message = Message.objects.create(
            sender_user=sender_user,
            receiver_user=receiver_user,
            room=current_room,
            message=message
        )
        new_message.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_name': sender_name
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender_name = event['sender_name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender_name': sender_name
        }))
