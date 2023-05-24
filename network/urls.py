
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
    path("follow/<str:name>", views.follow, name = "followapi"),
    path("currentuser", views.api_current_user, name = "currentUser"),
    path("following", views.following, name = "following")

]
