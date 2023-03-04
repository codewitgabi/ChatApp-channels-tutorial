import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
	def connect(self):
		""" Web socket connection hamdler. """
		self.accept() # accepts incoming connection
		
		""" send a response to the client """	
		self.send(json.dumps({
			"type": "connection_status",
			"status": "success",
			"response": "Connection to server is successful."
		}))
	
	def disconnect(self, close_code):
		""" Handles socket disconnection on our server """
		print(close_code)
	
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
		self.send(json.dumps({
			"type": "chat",
			"response": message
		}))
	