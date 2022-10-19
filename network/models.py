from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_following")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_follower")


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked")
