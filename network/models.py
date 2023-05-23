from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
    "self", blank=True, related_name="followers", symmetrical=False
    )

    liked = models.ManyToManyField(
    "self", blank = True, related_name = "likedback", symmetrical = False
    )


class Post(models.Model):
    owner = models.ForeignKey(User, related_name = "owner", on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"post by {self.owner}"
