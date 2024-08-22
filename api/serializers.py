from .models import BotUser
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class BotUserSerializer(ModelSerializer):
    class Meta:
        model = BotUser
        fields = ("name", "username", "user_id", "contact", "created_at", "code")
        
    def create(self, validated_data):
        return BotUser.objects.create(**validated_data)