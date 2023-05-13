# import asyncio
import json

# from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer

# from random import randint
# from time import sleep


class OrderConsumer(WebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": "Orders are connected!"
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        await self.send(text_data=json.dumps({
            "type": "order",
            "message": message
        }))