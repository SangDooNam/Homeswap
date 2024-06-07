# support/models.py
from django.conf import settings
from django.db import models
from accounts.models import AppUser
from messaging.models import Room

class SupportRequest(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Support Request from {self.email}'


class Deposit(models.Model):
    sender_user = models.ForeignKey(AppUser, related_name='room_sender_deposit', on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(AppUser,related_name='room_receiver_deposit', on_delete=models.CASCADE)
    room = room = models.ForeignKey(Room, related_name='chat_room_deposit', on_delete=models.CASCADE, null=True, blank=True)
    sender_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid_by_sender = models.BooleanField(default=False)
    is_paid_by_receiver = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {'Paid' if self.is_paid else 'Pending'}"

    @property
    def is_paid(self):
        return self.is_paid_by_sender  and self.is_paid_by_receiver
    
    @property
    def is_pending(self):
        return self.is_paid_by_sender or self.is_paid_by_receiver