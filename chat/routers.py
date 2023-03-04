from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
	re_path(r"ws/chat/(?P<room_name>\w+)/$",
		consumers.ChatConsumer.as_asgi(), name="ws_chat"),
	re_path(r"ws/cus/chat/(?P<room_name>\w+)/$",
		consumers.ChatConsumer.as_asgi(), name="ws_chat2"),
]