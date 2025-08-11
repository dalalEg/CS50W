from django.urls import path

from . import views
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("add", views.add, name="add"),
    path("random", views.random_entry, name="random"),
    path("search/", views.search, name="search"),
    path('edit/<str:entry>', views.edit, name='edit'),
    path("wiki/<str:title>", views.entry, name="entry"),   

]
