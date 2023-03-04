import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GroupChat, GroupMessage
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


class GroupChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user = self.scope.get("user")
		self.room = self.scope["url_route"]["kwargs"].get("room_name")
		self.group_name = f"chat_{self.room}"
		self.messages = await self.get_messages()
		
		await self.channel_layer.group_add(self.group_name, self.channel_name)
		
		await self.accept()
		
		await self.send(json.dumps({
			"type": "connection_status",
			"response": "Connected"
		}))
		
		await self.send(json.dumps({
			"type": "chat",
			"response": self.messages
		}))
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(self.group_name, self.channel_name)
	
	async def receive(self, text_data):
		msg = json.loads(text_data)
		await self.create_group_message(msg["message"])
		
		await self.channel_layer.group_send(
			self.group_name,
			{
				"type": "group_chat",
				"response": msg["message"]
			}
		)
		
	@database_sync_to_async
	def get_messages(self):
		self.group = GroupChat.objects.get(id=int(self.scope["url_route"]["kwargs"].get("room_name")))
		
		messages = list(self.group.groupmessage_set.all().values())
		
		for msg in messages:
			msg["sender"] = User.objects.get(id=msg["sender_id"]).username
			msg["date_created"] = str(msg["date_created"])
		
		return messages
	
	@database_sync_to_async
	def create_group_message(self, msg):
		group = self.group.groupmessage_set.create(
			group=self.group,
			sender=self.user,
			body=msg
		)
		group.save()
	
	async def group_chat(self, event):
		message = event["response"]
		self.messages = await self.get_messages()
		
		await self.send(text_data=json.dumps({"type": "chat", "response": self.messages}))

