from django.db import IntegrityError
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib. auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *

import json

def index(request):
    currentUser = request.user
    if Like.objects.filter(liker= currentUser).exists():    
        likedList = Like.objects.get(liker = currentUser)
        likedList = likedList.liked.all()
    else:
        f= Like(liker = currentUser)
        f.save()
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"posts": page_obj, "likes":likedList}
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
    if Following.objects.filter(follower = user).exists():
        followings = Following.objects.get(follower = currentUser)
        isFollowed = user in followings.following.all()
    else: 
        f = Following(follower = currentUser)
        f.save()
    context = {"profile": user, "isFollowed":isFollowed, "name":user.username, "following":Following.objects.filter(follower = user)}
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
    prof = User.objects.get(username = username)
    if request.method == "POST":
        if Following.objects.filter(follower = request.user).exists():
            user = Following.objects.get(follower = request.user)
            user.following.add(User.objects.get(username = username))
        else:
            f = Following(follower = request.user)
            f.save()
        return HttpResponseRedirect(reverse(f"core:profile", kwargs = {"name": prof.username}))    
    else:
        return HttpResponse("error")

def unfollow(request, username):
    prof = User.objects.get(username = username)
    if request.method == "POST":
        if Following.objects.filter(follower = request.user).exists():
            user = Following.objects.get(follower = request.user)
            user.following.remove(User.objects.get(username = username))
        else:
            f = Following(follower = request.user)
            f.save()
        return HttpResponseRedirect(reverse(f"core:profile", kwargs = {"name": prof.username}))    
    else:
        return HttpResponse("error")

def following(request):
    user = Following.objects.get(follower = request.user)
    posts= Post.objects.filter(owner__in=user.following).order_by('-timestamp') # showing followed user's posts
    context = {"posts":posts,"following":user}
    return render(request, "network/following.html", context)

@csrf_exempt
def editPost(request, post_id):
    post = Post.objects.filter(id = post_id)
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    if request.method =="POST":
        editedText = json_data.get("editedText", "")
        post.update(text=  editedText)
        return JsonResponse({"status":"edited successfully"})
    else:
        return JsonResponse({"error":"400"}, status = 400)

@csrf_exempt
def like(request, post_id):
    if not Like.objects.filter(liker = request.user).exists():
        f = Like(liker = user)
        f.save()
    data = request.body.decode('utf-8')
    # it takes request.user and relevant post and creates new Like model( user = request.user, post = post)
    post = Post.objects.get(id = post_id)
    user = request.user
    user_likes = Like.objects.get(liker = user)
    if request.method == "POST":
        if Like.objects.filter(liker = user).exists() and post in user_likes.liked.all():
            like = Like.objects.get(liker = user)
            like.liked.remove(post)
            return JsonResponse({"like":False})
        elif not post in user_likes.liked.all():
            like = Like.objects.get(liker = user)
            like.liked.add(post)
            return JsonResponse({"like":True})
    return JsonResponse({"error":"wrong method! Should be PUT"})