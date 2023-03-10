from django.urls import path
from . import views


urlpatterns = [
	path("", views.index, name="index"),
	path("signup", views.signup, name="signup"),
	path("signin/", views.signin, name="signin"),
	path("logout/", views.logout, name="logout"),
	path("group/<int:group_id>/", views.view_group, name="view_group"),
	path("user/chat/<int:receiver_id>/", views.user_to_user_chat, name="user_chat"),
]
