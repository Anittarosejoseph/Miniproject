from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('horofix/', consumers.ChatConsumer.as_asgi()),
]