from django.contrib import admin
from .models import GroupMessage, GroupChat, UserMessage


admin.site.register(GroupChat)
admin.site.register(GroupMessage)
admin.site.register(UserMessage)