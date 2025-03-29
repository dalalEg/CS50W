from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listingPage/<int:auction_id>", views.listingPage, name="listingPage"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("profile", views.profile, name="profile"),
    path("changePassword", views.changePassword, name="changePassword"),
    path("addCategory", views.addCategory, name="addCategory"),
    path("closed/<int:auction_id>", views.closed, name="close"),
    path("profile/bids", views.bids, name="bids"),
    path("profile/won", views.won, name="won"),
    path("profile/listing", views.auctions, name="listing"),
    path("profile/comments", views.comments, name="comments"),
    path("search", views.search, name="search"),
]
