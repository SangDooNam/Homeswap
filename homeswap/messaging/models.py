from django.db import models
from accounts.models import AppUser
from django.core.exceptions import ValidationError


class Room(models.Model):
    sender_user = models.ForeignKey(AppUser, related_name='room_sender', on_delete=models.SET_NULL, null=True)
    receiver_user = models.ForeignKey(AppUser, related_name='room_receiver', on_delete=models.SET_NULL, null=True)
    room_name = models.CharField(max_length=100, unique=True)
    sender_confirmed = models.BooleanField(default=False)
    receiver_confirmed = models.BooleanField(default=False)
    
    @property
    def is_confirmed(self):
        return self.sender_confirmed and self.receiver_confirmed

    def __str__(self):
        return self.room_name

class Message(models.Model):
    sender_user = models.ForeignKey(AppUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(AppUser, related_name='received_messages', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='chat_room', on_delete=models.CASCADE, null=True, blank=True)
    message= models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class ReportUser(models.Model):
    reporter = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='subject')
    reported = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='object')
    block = models.BooleanField(default=False)
    report_message = models.TextField(null=True, blank=True)

