import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from chat_control.models import Message


class ChatHomeConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.user = None
        self.receiver = None

    async def connect(self):
        self.user = self.scope["user"]
        # print(request_user)
        if self.user.is_authenticated:
            self.receiver = self.scope["url_route"]["kwargs"]["id"]
            self.receiver_user_id = int(self.receiver)
            user_ids = [int(self.user.id), int(self.receiver)]
            user_ids = sorted(user_ids)
            self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        if not message or len(message) > 500:
            return
        message_obj = await self.create_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_obj.content,
                "timestamp": str(message_obj.timestamp),
            },
        )

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        message = event["message"]
        timestamp = event["timestamp"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "timestamp": timestamp,
                }
            )
        )

    @database_sync_to_async
    def create_message(self, message):
        try:
            return Message.objects.create(
                user_id=self.user.id, content=message, receiver_id=self.receiver
            )
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
