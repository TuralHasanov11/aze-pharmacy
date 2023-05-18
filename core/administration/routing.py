from administration import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/order-socket-server/', consumers.OrderConsumer.as_asgi())
]