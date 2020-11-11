from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_, name="login"),
    path("logout/", views.logout_, name="logout"),
    path("register/", views.register, name="register"),
    path("new-post/", views.newPost, name="newPost"),
    path("following/", views.following, name="following"),
    path("like/", views.likePost, name="like"),
    path("liked/", views.haveLiked, name="liked"),
    path("users/<str:username>/follow/", views.toggleFollowing, name="toggleFollowing"),
    path("users/<str:username>/", views.profile, name="profile"),
    path("edit/", views.editPost, name="editPost"),
    path("delete/", views.deletePost, name="deletePost")
]