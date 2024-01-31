import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from chat_control.models import Message


class ChatHomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_user = self.scope["user"]
        # print(request_user)
        if request_user.is_authenticated:
            chat_with_user = self.scope["url_route"]["kwargs"]["id"]
            self.receiver_user_id = int(chat_with_user)
            user_ids = [int(request_user.id), int(chat_with_user)]
            user_ids = sorted(user_ids)
            self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        receiver_user_id = self.receiver_user_id
        await self.channel_layer.send(
            "store_message",  # Channel name for message storage
            {
                "type": "store.message",
                "message": message,
                "sender_user_id": self.scope["user"].id,
                "receiver_user_id": receiver_user_id,
                "room_name": self.room_group_name,
            },
        )
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    class MessageStorageConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            await self.accept()

        async def disconnect(self, close_code):
            pass

        async def store_message(self, event):
            message = event["message"]
            sender_user_id = event["sender_user_id"]
            receiver_user_id = event["receiver_user_id"]
            room_name = event["room_name"]

            # Use database_sync_to_async to make a synchronous database call
            # Save the message in your Message model
            await database_sync_to_async(Message.objects.create)(
                sender_id=sender_user_id,  # Assuming your Message model has a "sender" field
                receiver_id=receiver_user_id,  # Assuming your Message model has a "receiver" field
                message=message,
            )
