from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StoredEmail
from .models import Message


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "id"]
        extra_kwargs = {"id": {"read_only": True}}


class StoredEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredEmail
        fields = ["email", "user"]
        extra_kwargs = {"user": {"read_only": True}}


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "receiver_id", "user_id", "content", "timestamp")
        read_only_fields = ("id", "timestamp")
