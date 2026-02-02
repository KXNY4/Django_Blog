from django.urls import path
from .views import PostListView, PostDetailView, MyPostsView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('my/', MyPostsView.as_view(), name='my-posts'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]