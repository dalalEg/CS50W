from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("posts/", views.posts, name="post"),
    path("api/profile/", views.profile, name="profile"), 
    path("api/profile/<str:username>/", views.other_profile, name='profile'),
    path("api/profile/<str:username>/posts/", views.userPosts, name='follow_user'),
    path("api/profile/<str:username>/followers/", views.profile, name='follow_user'),
    path("api/profile/<str:username>/following/", views.profile, name='follow_user'),
    path("api/profile/<str:username>/comments/", views.user_comments, name="user_comments"),
    path("api/profile/<str:username>/likes/", views.user_likes, name="user_likes"),
    path("api/posts/", views.posts, name="posts"),
    path("api/following/", views.following, name="following"),
    path("api/posts/<int:post_id>/", views.post, name="post_detail"),
    path("api/posts/<int:post_id>/like/", views.like_post, name="like_post"),
    path("api/posts/<int:post_id>/comment/", views.comment, name="comment_post"),
    path("api/search/", views.search, name="search"),
    # to refresh the page
    re_path(r'^(?!api/).*$', views.spa_shell, name="spa_shell"),
]
