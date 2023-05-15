import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class OrderConsumer(AsyncJsonWebsocketConsumer):
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