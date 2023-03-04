from django.contrib import admin
from django.urls import path, include
from chat import views as chat_views


urlpatterns = [
	path('admin/', admin.site.urls),
	path("", chat_views.chat, name="chat"),
	path("room/<str:room_name>/", chat_views.room, name="room"),
	path("main/", include("main.urls")),
]
