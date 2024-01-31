from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import status
from django.shortcuts import get_object_or_404
from chat_control.serializers import UserGetSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .models import Message, StoredEmail
from .serializers import MessageSerializer, StoredEmailSerializer
from django.db import IntegrityError
from django.db import models

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
            {"error": f"{email} does not exist"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def store_email(request):
    email = request.data.get("email")
    if email:
        try:
            user_obj = get_object_or_404(User, email=email)
            serializer = UserGetSerializer(user_obj)
            stored_email = StoredEmail(
                email=serializer.data["email"], user=serializer.data["id"]
            )
            stored_email.save()
            return Response(
                {"message": "Email stored successfully"}, status=status.HTTP_201_CREATED
            )
        except IntegrityError as e:
            return Response(
                {"error": f"You have added {email} already"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_emails(request):
    if request.method == "GET":
        stored_emails = StoredEmail.objects.all()
        serializer = StoredEmailSerializer(stored_emails, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    ordering = ("-timestamp",)

    def get_queryset(self):
        user_id = self.request.user.id
        partner_id = self.kwargs["partner_id"]  # Adjust based on your URL pattern

        queryset = Message.objects.filter(
            (models.Q(user=user_id) & models.Q(receiver=partner_id))
            | (models.Q(user=partner_id) & models.Q(receiver=user_id))
        ).order_by("timestamp")

        return queryset
