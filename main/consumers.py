import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GroupChat, GroupMessage, UserMessage
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import secrets


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


class UserChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		
		self.messages = await self.get_users_messages()
		
		self.user = self.scope.get("user")
		self.receiver_id = self.scope["url_route"]["kwargs"].get("receiver_id")
		
		unique_id = "".join(sorted(self.receiver_id + str(self.user.id)))
		
		self.receiver = await self.get_receiver()
		self.group_name = f"user_chat_{unique_id}"
		
		print(self.group_name)
		
		await self.channel_layer.group_add(
			self.group_name,
			self.channel_name
		)
		
		await self.send(json.dumps({
			"type": "chat",
			"response": self.messages
		}))
		
		await self.send(
			json.dumps({
				"type": "conn",
				"response": "Connected"
			})		
		)
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(self.group_name, self.channel_name)
	
	async def receive(self, text_data):
		data = json.loads(text_data)
		
		await self.create_users_message(data.get("message"))
		
		await self.channel_layer.group_send(
			self.group_name,
			{
				"type": "broadcast_message",
				"response": data.get("message")
			}
		)
	
	@database_sync_to_async
	def get_receiver(self):
		receiver = User.objects.get(id= self.receiver_id)
		return receiver.username
	
	@database_sync_to_async
	def create_users_message(self, msg):
		receiver_id = self.scope["url_route"]["kwargs"].get("receiver_id")
		receiver = User.objects.get(id= receiver_id)
		message = UserMessage.objects.create(
			sender=self.scope.get("user"),
			receiver=receiver,
			message=msg
		)
		message.save()
	
	@database_sync_to_async
	def get_users_messages(self):
		receiver_id = self.scope["url_route"]["kwargs"].get("receiver_id")
		receiver = User.objects.get(id= receiver_id)
		sender_messages = UserMessage.objects.filter(
			sender=self.scope.get("user"), receiver=receiver)
		receiver_messages = UserMessage.objects.filter(
			sender=receiver, receiver=self.scope.get("user"))
		
		messages = sender_messages.union(receiver_messages).order_by("date_created")
		messages = list(messages.values())
		
		for msg in messages:
			msg["sender"] = User.objects.get(id=msg["sender_id"]).username
			msg["date_created"] = str(msg["date_created"])
		
		return messages
	
	async def broadcast_message(self, event):
		messages = await self.get_users_messages()
		
		await self.send(text_data=json.dumps({
			"type": "chat",
			"response": messages
		}))
