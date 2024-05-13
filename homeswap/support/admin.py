from django.contrib import admin
from .models import SupportRequest

class SupportAdmin(admin.ModelAdmin):
	list_display = ('email', 'subject', 'message', 'created_at')
	search_fields = ('subject', 'sender__username', 'recipient__username', 'body')

admin.site.register(SupportRequest, SupportAdmin)
# Register your models here.
