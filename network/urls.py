
from django.urls import path

from . import views

app_name ="core"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createPost, name = "createPost"),
    path("profile/<str:name>", views.profile, name = "profile"),
    path("follow/<str:username>", views.follow, name ="follow"),
    path("unfollow/<str:username>", views.unfollow, name ="unfollow"),
    path("following", views.following, name = "following"),
    path("edit/<int:post_id>", views.editPost, name ="edit"),
    path("like/<int:post_id>", views.like, name = "like")
]
