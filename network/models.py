from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey(User, related_name = "owner", on_delete=models.CASCADE)
    photo = models.ImageField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"post by "

class Like(models.Model):
    post = models.ForeignKey(Post, related_name = "liked", on_delete = models.CASCADE)
    owner = models.ForeignKey(User, related_name = "liker",  on_delete = models.CASCADE)

class Following(models.Model):
    follower = models.OneToOneField(User, related_name = "follower", on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name = "following", )


    def __str__(self):
        return f"{self.folloewer} following {self.following}"