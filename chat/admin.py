from django.contrib import admin
from chat.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "reciever", "message", "seen", "created_at"]
