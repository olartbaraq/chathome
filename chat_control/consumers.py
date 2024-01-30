from channels.generic.websocket import AsyncWebsocketConsumer


class ChatHomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("TESTING CONNECTION AND REDIS")
        await self.accept()
