import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class OrderConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'orders'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": self.channel_name
        }))

    async def disconnect(self, *args, **kwargs):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        await self.channel_layer.group_send(self.group_name, {
            "type": "order_created",
            "message": data["message"]
        })

    async def order_created(self, event, type='order_created'):
        print(event)
        await self.send(text_data=json.dumps({'message': event['message'], 'type': type}))

        