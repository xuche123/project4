from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
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
    # following = False
    
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
def follow(request):
    if request.method == 'POST':
        follow = json.loads(request.body)['follow']
        follow = User.objects.get(username=follow)

        exist = Follow.objects.filter(follower=request.user, following=follow)
        if not exist:
            follow = Follow(follower=request.user, following=follow)
            follow.save()
            return JsonResponse({"type": "follow"}, status=201)
        else:
            exist.delete()
            return JsonResponse({"type": "unfollow"}, status=201)


def following(request):
    following = Follow.objects.filter(follower=request.user).values('following')
    following_list = [User.objects.get(id=following[i]['following']) for i in range(len(following))]
    print(following_list)
    
    posts = Post.objects.filter(user__in=following).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })
