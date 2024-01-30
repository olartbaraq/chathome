from django.urls import path
from .consumers import ChatHomeConsumer

websocket_urlpatterns = [path("ws/chat/", ChatHomeConsumer.as_asgi())]
