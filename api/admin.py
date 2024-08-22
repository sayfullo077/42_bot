from django.contrib import admin
from .models import BotUser

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "name", "username", "contact", "code", "created_at"]