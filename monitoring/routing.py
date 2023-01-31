from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/", consumers.StreamConsumer.as_asgi()),
]
