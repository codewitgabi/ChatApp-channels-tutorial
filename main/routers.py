from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
	re_path(r"ws/main/chat/(?P<room_name>\w+)/$",
		consumers.GroupChatConsumer.as_asgi(), name="ws_group_chat"),
]