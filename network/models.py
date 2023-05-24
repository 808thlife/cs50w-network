from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField(
    "self", blank=True, related_name="followers", symmetrical=False
    )


class Post(models.Model):
    owner = models.ForeignKey(User, related_name = "owner", on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"post by {self.owner}"

class Like(models.Model):
    liker = models.ForeignKey(User, related_name = "liker", on_delete = models.CASCADE)
    liked = models.ForeignKey(Post, related_name = "liked", on_delete = models.CASCADE)

class Following(models.Model):
    following = models.ForeignKey(User, related_name = "fwing", on_delete=models.CASCADE)
    followers = models.ForeignKey(User, related_name = "fwers", on_delete=models.CASCADE)