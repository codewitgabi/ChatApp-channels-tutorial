from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *


def index(request):
	groups = GroupChat.objects.all()
	return render(request, "index.html", {"groups": groups})
	

def signup(request):
	if request.user.is_authenticated:
		return redirect("index")
		
	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password1 = request.POST.get("password1")
		password2 = request.POST.get("password2")
		
		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.error(request, "User with given username already exists")
			elif User.objects.filter(email=email).exists():
				messages.error(request, "User with given email already exists")
			else:
				User.objects.create_user(
					username=username,
					email=email,
					password=password1)
				messages.info(request, f"Account for {username} created successfully!!")
				return redirect("signin")
		else:
			messages.error(request, "Passwords do not match")
		
	return render(request, "signup.html")


def signin(request):
	if request.user.is_authenticated:
		return redirect("index")
		
	if request.method == "POST":
		username = request.POST.get("username")
		password1 = request.POST.get("password1")
		
		user = auth.authenticate(username=username, password=password1)
		
		if user is not None:
			auth.login(request, user)
			messages.info(request, request.user)
			return redirect("index")
		else:
			messages.error(request, "Incorrect username or password")
			return redirect("signin")
		
	return render(request, "signin.html")


def logout(request):
	auth.logout(request)
	return redirect("signup")


def view_group(request, group_id):
	group = GroupChat.objects.get(id=group_id)
	return render(request, "group_detail.html", {"group": group})

