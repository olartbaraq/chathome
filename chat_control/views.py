from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework import status
from django.shortcuts import get_object_or_404
from chat_control.serializers import UserGetSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_lists(request: Request):
    try:
        user_obj = User.objects.exclude(id=request.user.id)
        serializer = UserGetSerializer(user_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Error listing users"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request: Request, email: str):
    try:
        user_obj = get_object_or_404(User, email=email)
        serializer = UserGetSerializer(user_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"Error listing user {email}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
