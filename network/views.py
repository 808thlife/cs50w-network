from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *

import json

def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    context = {"posts": posts}
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("core:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("core:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("core:index"))
    else:
        return render(request, "network/register.html")

def createPost(request):
    if request.method == "POST":
        text = request.POST.get("post-text")
        owner = request.user
        f = Post(text = text, owner = owner )
        f.save()
        return HttpResponseRedirect(reverse("core:index"))

def profile(request, name):
    user = User.objects.get(username = name)
    currentUser = request.user
    isFollowed = user in currentUser.following.all()
    context = {"profile": user, "isFollowed":isFollowed, "name":user.username}
    return render(request,"network/profile.html", context)

def follow(request, name):
    user = User.objects.filter(username = name).values()
    if request.method == "PUT":
        return JsonResponse(user, safe = False)
        
def api_current_user(request):
    user = list(User.objects.filter(pk=request.user.pk).values(
        "username"
    ))
    return JsonResponse(user, safe = False)

def follow(request, username):
    user = User.objects.get(username = username)
    currentUser = request.user
    user.following.add(currentUser)
    return HttpResponseRedirect(reverse(f"core:profile", kwargs = {"name": user}))

def unfollow(request, username):
    user = User.objects.get(username = username)
    currentUser = request.user
    user.following.remove(currentUser)
    return HttpResponseRedirect(reverse(f"core:profile", kwargs = {"name": user}))

def following(request):
    currentUser = request.user
    following = currentUser.following.all()
    posts= Post.objects.filter(owner__in= following).order_by('-timestamp') # showing followed user's posts
    context = {"posts":posts}
    return render(request, "network/following.html", context)

