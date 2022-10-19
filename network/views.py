from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import Follow, User, Post
from .forms import PostForm


def index(request):
    if request.method == "POST":
        post = Post(user=request.user)
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        post_form = PostForm()
        posts = Post.objects.all().order_by("-timestamp")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "post_form": post_form,
            "page_obj": page_obj
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    view_user = User.objects.get(username=username)
    posts = Post.objects.filter(user=view_user).order_by("-timestamp")
    exist = Follow.objects.filter(follower=request.user, following=view_user)
    if exist:
        following = True
    else:
        following = False

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "view_user": view_user,
        "page_obj": page_obj,
        'following': following
    })

@csrf_exempt
@login_required
def follow(request):
    if request.method == 'POST':
        follow = json.loads(request.body)['follow']
        follow = User.objects.get(username=follow)
        
        exist = Follow.objects.filter(follower=request.user, following=follow)
        
        if not exist:
            follow_obj = Follow(follower=request.user, following=follow)
            follow_obj.save()
            follower_count=follow.user_follower.count()
            return JsonResponse({"type": "follow", "follower_count": follower_count}, status=201)
        else:
            exist.delete()
            follower_count=follow.user_follower.count()
            return JsonResponse({"type": "unfollow", "follower_count": follower_count}, status=201)

@csrf_exempt
@login_required
def like(request):
    if request.method == "POST":
        post_id = json.loads(request.body)["post_id"]
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            post.save()
            count = post.likes.count()
            return JsonResponse({"type": "unlike", "count": count}, status=201)
        else:
            post.likes.add(user)
            post.save()
            count = post.likes.count()
            return JsonResponse({"type": "like", "count": count}, status=201)

@csrf_exempt
@login_required
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data["post_id"]
        post = Post.objects.get(id=post_id)
        post.content = data["content"]
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)

def following(request):
    following = Follow.objects.filter(follower=request.user).values('following')
    posts = Post.objects.filter(user__in=following).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })
