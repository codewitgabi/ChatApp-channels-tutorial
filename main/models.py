from django.db import models
from django.contrib.auth.models import User


class GroupChat(models.Model):
	name = models.CharField(max_length=30)
	participants = models.ManyToManyField(User, null=True, blank=True)
	
	def __str__(self):
		return self.name
		

class GroupMessage(models.Model):
	body = models.TextField()
	group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
	sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	date_created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.body


