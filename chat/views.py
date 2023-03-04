from django.shortcuts import render, redirect


def chat(request):
	if request.method == "POST":
		return redirect("room", room_name=request.POST.get("room_name"))
	return render(request, "chat.html")


def room(request, room_name):
	return render(request, "room.html", {"room_name": room_name})

