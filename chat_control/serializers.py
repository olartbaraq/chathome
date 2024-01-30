from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StoredEmail


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "id"]
        extra_kwargs = {"id": {"read_only": True}}


class StoredEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredEmail
        fields = ["email"]
