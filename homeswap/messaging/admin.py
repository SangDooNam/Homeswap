from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'sent_at', 'read_at')
    search_fields = ('subject', 'sender__username', 'recipient__username', 'body')

admin.site.register(Message, MessageAdmin)


