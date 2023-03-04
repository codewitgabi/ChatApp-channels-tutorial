import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
	def connect(self):
		""" Get the room name """
		self.room = self.scope["url_route"]["kwargs"].get("room_name")
		""" Create a group """
		self.room_group_name = f"chat_{self.room}"
		
		""" Add the client to the group """
		async_to_sync(self.channel_layer.group_add) (
			self.room_group_name, self.channel_name
		)
		
		""" Web socket connection hamdler. """
		self.accept() # accepts incoming connection
		
		""" send a response to the client """	
		self.send(json.dumps({
			"type": "connection_status",
			"status": "success",
			"response": "Connection to server is successful."
		}))
	
	def disconnect(self, close_code):
		"""
			Handles socket disconnection on our server.
			Once the client closes connection, we remove them from the group.
		"""
		async_to_sync(self.channel_layer.group_discard) (
			self.room_group_name, self.channel_name
		)
	
	def receive(self, text_data):
		"""
			Handles incoming data from client.
			Note that the variable <text_data> cannot be renamed. It should be passed as text_data.
		"""
		json_data = json.loads(text_data)
		message = json_data.get("message")
		
		"""
			Return the sent message back to the client
		"""
		"""
		self.send(json.dumps({
			"type": "chat",
			"response": message
		}))
		"""
		
		async_to_sync(self.channel_layer.group_send) (
			self.room_group_name, {"type": "group_chat", "response": message}
		)
	
	def group_chat(self, event):
		message = event["response"]
		
		self.send(text_data=json.dumps({"type": "chat", "response": message}))
	