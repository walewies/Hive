from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("new-post/", views.CreatePost.as_view(), name="new_post"),
    path("post-<int:pk>/", views.PostView.as_view(), name="view_post")
]