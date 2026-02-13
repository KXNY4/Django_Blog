from django.urls import path
from .views import CategoryDetailView, CategoryListView, PostLikeView, PostListView, PostDetailView, MyPostsView, TagDetailView, TagListView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('my/', MyPostsView.as_view(), name='my-posts'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag-detail'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('<slug:slug>/like/', PostLikeView.as_view(), name='post-like'),
]